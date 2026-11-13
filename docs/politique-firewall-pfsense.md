# Politique de pare-feu pfSense — Drakonis

## Principe : deny by default + liste blanche par VLAN

Chaque interface se termine par un **deny all** explicite et journalisé. On n'ouvre que ce qui est nécessaire au métier du segment. Tout est journalisé sauf le trafic courant (DNS, ICMP vers la passerelle).

> **Rappel pfSense :** les règles s'appliquent au trafic **entrant** sur l'interface, de haut en bas, et la première règle qui correspond l'emporte.

---

## 1. Alias

### Alias réseau

| Nom | Contenu | Description |
|-----|---------|-------------|
| `Reseaux_Internes` | 10.0.0.0/8, 172.16.0.0/12, 192.168.0.0/16 | RFC 1918 |
| `VLAN_IT` | 10.10.0.0/16 | IT / administration |
| `VLAN_Users` | 10.20.0.0/16 | Métiers (RH, compta, ventes, direction, créa) |
| `VLAN_Logistics` | 10.30.0.0/16 | Logistique |
| `VLAN_Guests` | 10.50.0.0/16 | Invités |
| `VLAN_DMZ` | 10.100.0.0/16 | DMZ (web public) |
| `VLAN_Infra` | 10.110.0.0/16 | Management (pare-feu, routeurs, switches) |
| `VLAN_Services` | 10.120.0.0/16 | Serveurs (AD, SIEM, fichiers, NAS) |
| `Serveurs_Internes` | 10.110.0.0/16, 10.120.0.0/16 | Infra + Services |

### Alias de ports

| Nom | Ports | Description |
|-----|-------|-------------|
| `Ports_AD` | 53, 88, 135, 389, 445, 636, 3268, 3269 | DNS, Kerberos, RPC, LDAP, SMB, LDAPS, catalogue global |
| `Ports_Web` | 80, 443 | HTTP / HTTPS |
| `Ports_Monitoring` | 1514, 1515, 55000 | Agents Wazuh → manager |
| `Ports_SSH` | 22 | SSH |
| `Ports_RDP` | 3389 | Bureau à distance |
| `Ports_Zabbix` | 10050, 10051 | Agent / serveur Zabbix |

---

## 2. Règles par interface

### IT (VLAN 10) — administrateurs
L'IT accède à tout ce qu'il administre, mais tout accès d'administration est journalisé.

| # | Action | Proto | Source | Destination | Port | Log | Description |
|---|---|---|---|---|---|---|---|
| 1 | Pass | ICMP | IT net | * | * | Non | Ping |
| 2 | Pass | TCP/UDP | IT net | VLAN_Services | Ports_AD | Non | Authentification, DNS, GPO |
| 3 | Pass | TCP | IT net | VLAN_Services | Ports_SSH, Ports_RDP | Oui | Administration des serveurs |
| 4 | Pass | TCP | IT net | VLAN_Infra | Ports_Web, Ports_SSH | Oui | Administration pfSense, switches |
| 5 | Pass | TCP/UDP | IT net | VLAN_DMZ | * | Oui | Administration DMZ |
| 6 | Pass | TCP/UDP | IT net | VLAN_Services | Ports_Monitoring, Ports_Zabbix | Non | Supervision |
| 7 | Pass | TCP/UDP | IT net | ! Reseaux_Internes | * | Non | Internet |
| 8 | Block | * | IT net | * | * | Oui | Deny all |

### Métiers (VLAN 20)
AD, partage de fichiers, site interne, Internet. Aucun accès d'administration.

| # | Action | Proto | Source | Destination | Port | Log | Description |
|---|---|---|---|---|---|---|---|
| 1 | Pass | ICMP | USERS net | USERS address | * | Non | Ping passerelle |
| 2 | Pass | TCP/UDP | USERS net | VLAN_Services | Ports_AD | Non | AD (auth, DNS, GPO, SMB) |
| 3 | Pass | TCP | USERS net | VLAN_DMZ | Ports_Web | Non | Site web interne |
| 4 | Block | * | USERS net | Reseaux_Internes | * | Oui | **Tout autre trafic interne** |
| 5 | Pass | TCP/UDP | USERS net | * | Ports_Web, 53 | Non | Internet (HTTP/S + DNS) |
| 6 | Block | * | USERS net | * | * | Oui | Deny all |

> La règle 4 **doit** précéder la règle 5 : sinon un utilisateur atteindrait n'importe quel port interne 80/443 via la règle Internet.

### Logistique (VLAN 30)
Même logique que les Métiers.

| # | Action | Proto | Source | Destination | Port | Log | Description |
|---|---|---|---|---|---|---|---|
| 1 | Pass | ICMP | LOGISTICS net | LOGISTICS address | * | Non | Ping passerelle |
| 2 | Pass | TCP/UDP | LOGISTICS net | VLAN_Services | Ports_AD | Non | AD |
| 3 | Pass | TCP | LOGISTICS net | VLAN_DMZ | Ports_Web | Non | Portail web interne |
| 4 | Block | * | LOGISTICS net | Reseaux_Internes | * | Oui | Tout autre trafic interne |
| 5 | Pass | TCP/UDP | LOGISTICS net | * | Ports_Web, 53 | Non | Internet |
| 6 | Block | * | LOGISTICS net | * | * | Oui | Deny all |

### Invités (VLAN 50)
Aucun accès interne. Internet uniquement.

| # | Action | Proto | Source | Destination | Port | Log | Description |
|---|---|---|---|---|---|---|---|
| 1 | Pass | ICMP | GUESTS net | GUESTS address | * | Non | Ping passerelle |
| 2 | Block | * | GUESTS net | Reseaux_Internes | * | Oui | Tout trafic interne |
| 3 | Pass | TCP | GUESTS net | * | Ports_Web | Non | Internet HTTP/S |
| 4 | Pass | UDP | GUESTS net | * | 53 | Non | DNS |
| 5 | Block | * | GUESTS net | * | * | Oui | Deny all |

> Un invité navigue sur Internet mais ne voit aucune ressource interne, même en scan.

### DMZ (VLAN 100) — serveur web
La DMZ n'initie que vers la base de données, le DNS, le SIEM et Internet (mises à jour).

| # | Action | Proto | Source | Destination | Port | Log | Description |
|---|---|---|---|---|---|---|---|
| 1 | Pass | TCP | DMZ net | VLAN_Services | 3306, 5432 | Oui | Base de données |
| 2 | Pass | TCP/UDP | DMZ net | VLAN_Services | 53 | Non | DNS |
| 3 | Pass | TCP | DMZ net | VLAN_Services | Ports_Monitoring | Non | Envoi des journaux à Wazuh |
| 4 | Block | * | DMZ net | Reseaux_Internes | * | Oui | **Pas de pivot vers l'interne** |
| 5 | Pass | TCP | DMZ net | * | Ports_Web | Non | Mises à jour |
| 6 | Block | * | DMZ net | * | * | Oui | Deny all |

> Si le serveur web est compromis, l'attaquant ne peut joindre que la base de données. La règle 4 bloque le mouvement latéral.

### Management (VLAN 110)
Seul l'IT y accède. L'infrastructure n'initie presque rien.

| # | Action | Proto | Source | Destination | Port | Log | Description |
|---|---|---|---|---|---|---|---|
| 1 | Pass | TCP/UDP | INFRA net | VLAN_Services | 53 | Non | DNS |
| 2 | Pass | TCP | INFRA net | VLAN_Services | Ports_Monitoring | Non | Wazuh / Zabbix |
| 3 | Block | * | INFRA net | Reseaux_Internes | * | Oui | Aucun autre VLAN |
| 4 | Pass | TCP | INFRA net | * | Ports_Web | Non | Mises à jour firmware |
| 5 | Block | * | INFRA net | * | * | Oui | Deny all |

### Serveurs (VLAN 120) — DC, SIEM, fichiers, NAS
Les serveurs n'initient pas de connexion vers les postes clients.

| # | Action | Proto | Source | Destination | Port | Log | Description |
|---|---|---|---|---|---|---|---|
| 1 | Pass | TCP/UDP | SERVICES net | VLAN_Services | * | Non | Intra-VLAN (réplication AD…) |
| 2 | Pass | TCP | SERVICES net | * | Ports_Web, 53 | Non | Mises à jour, DNS externe |
| 3 | Block | * | SERVICES net | Reseaux_Internes | * | Oui | Pas d'initiation vers les postes |
| 4 | Block | * | SERVICES net | * | * | Oui | Deny all |

> Un DC compromis ne peut ni scanner ni pivoter vers les postes utilisateurs depuis le VLAN Serveurs.

### WAN — entrant

| # | Action | Proto | Source | Destination | Port | Log | Description |
|---|---|---|---|---|---|---|---|
| 1 | Block | * | RFC 1918 | * | * | Oui | Anti-usurpation |
| 2 | Pass | TCP | * | Serveur web DMZ | 80, 443 | Oui | Redirection de port (NAT) |

---

## 3. Ordre de mise en œuvre

1. Créer tous les alias.
2. Invités (le plus simple), puis Métiers et Logistique.
3. DMZ (le plus critique).
4. Serveurs et Management.
5. IT en dernier (le plus permissif).
6. Tester après chaque VLAN.

## 4. Tests de validation (pour chaque VLAN)

```
✅ Ping de sa passerelle            → passe
✅ Ping 8.8.8.8                     → passe (sauf Management/Serveurs selon la politique)
✅ Résolution DNS via le DC         → passe pour les VLAN authentifiés
❌ Ping vers un VLAN non autorisé    → bloqué ET visible dans les journaux
❌ SSH vers un serveur (hors IT)     → bloqué
```

## 5. En une phrase

Moindre privilège par segment : chaque VLAN n'accède qu'à ce dont son métier a besoin, la DMZ ne peut pas pivoter, et seul l'IT a un accès élargi, tracé et journalisé.
