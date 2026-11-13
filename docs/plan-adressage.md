# Plan d'adressage IPv4 — Drakonis (v3)

**Convention :** `10.[VLAN].[fonction].[hôte]/24` — supernet 10.0.0.0/8 — VIP HSRP = `.1`, R1 = `.2`, R2 = `.3`, VIP CARP pfSense = `.254` (VLAN 110 uniquement).

## VLAN

| VLAN | Nom | Bloc | Sous-réseau | Fonction | Passerelle HSRP | Notes |
|---|---|---|---|---|---|---|
| 10 | IT | 10.10.0.0/16 | 10.10.0.0/24 | Réservé HSRP / routage | 10.10.0.1 | R1=.2 R2=.3 |
| 10 | IT | 10.10.0.0/16 | 10.10.1.0/24 | SysAdmins (3 postes) | 10.10.0.1 | Croissance prévue |
| 10 | IT | 10.10.0.0/16 | 10.10.2.0/24 | Dev (3 postes) | 10.10.0.1 |  |
| 10 | IT | 10.10.0.0/16 | 10.10.3.0/24 | Réservé (nouveaux pôles IT) | 10.10.0.1 | Sécurité, DevOps... |
| 20 | Métiers | 10.20.0.0/16 | 10.20.0.0/24 | Réservé HSRP / routage | 10.20.0.1 |  |
| 20 | Métiers | 10.20.0.0/16 | 10.20.1.0/24 | Marketing/Creatives (7) | 10.20.0.1 |  |
| 20 | Métiers | 10.20.0.0/16 | 10.20.2.0/24 | Sales (3) | 10.20.0.1 |  |
| 20 | Métiers | 10.20.0.0/16 | 10.20.3.0/24 | Management/Direction (3) | 10.20.0.1 |  |
| 20 | Métiers | 10.20.0.0/16 | 10.20.4.0/24 | RH (2) | 10.20.0.1 |  |
| 20 | Métiers | 10.20.0.0/16 | 10.20.5.0/24 | Comptabilité (2) | 10.20.0.1 |  |
| 30 | Logistique | 10.30.0.0/16 | 10.30.0.0/24 | Réservé HSRP | 10.30.0.1 |  |
| 30 | Logistique | 10.30.0.0/16 | 10.30.1.0/24 | Postes logistique (12) | 10.30.0.1 |  |
| 30 | Logistique | 10.30.0.0/16 | 10.30.2.0/24 | Douchettes code-barres (DHCP) | 10.30.0.1 | Pool DHCP |
| 50 | Guest WiFi | 10.50.0.0/24 | 10.50.0.0/24 | Réservé HSRP + pool DHCP | 10.50.0.1 | Isolé Internet only |
| 100 | DMZ | 10.100.0.0/16 | 10.100.0.0/24 | Réservé HSRP | 10.100.0.1 |  |
| 100 | DMZ | 10.100.0.0/16 | 10.100.1.0/24 | VPN gateway (10.100.1.1) | 10.100.0.1 | WireGuard |
| 100 | DMZ | 10.100.0.0/16 | 10.100.2.0/24 | Web frontaux e-commerce | 10.100.0.1 | Reverse proxy nginx |
| 100 | DMZ | 10.100.0.0/16 | 10.100.3.0/24 | Mail relay / Bastion SSH | 10.100.0.1 |  |
| 110 | Management | 10.110.0.0/16 | 10.110.0.0/24 | Réservé HSRP gateway | 10.110.0.1 |  |
| 110 | Management | 10.110.0.0/16 | 10.110.1.0/24 | Firewalls pfSense | 10.110.0.1 | pfSense ext .1 + .2 (CARP), VIP .254 / pfSense int .21 |
| 110 | Management | 10.110.0.0/16 | 10.110.2.0/24 | Routeurs core | 10.110.0.1 | R1=.1 R2=.2 |
| 110 | Management | 10.110.0.0/16 | 10.110.3.0/24 | Switches L2 | 10.110.0.1 | IOU1=.10 IOU2=.20 IOU3=.30 IOU4=.40 |
| 110 | Management | 10.110.0.0/16 | 10.110.4.0/24 | Hyperviseurs / VM hosts | 10.110.0.1 | GNS3 server, VMware |
| 120 | Serveurs | 10.120.0.0/16 | 10.120.0.0/24 | Réservé HSRP | 10.120.0.1 |  |
| 120 | Serveurs | 10.120.0.0/16 | 10.120.1.0/24 | SIEM — Wazuh (10.120.1.1) | 10.120.0.1 | Manager + indexer + dashboard |
| 120 | Serveurs | 10.120.0.0/16 | 10.120.2.0/24 | NAS Backup (10.120.2.1) | 10.120.0.1 | Cible Restic |
| 120 | Serveurs | 10.120.0.0/16 | 10.120.3.0/24 | AD / DNS — DC1=.1 DC2=.2 | 10.120.0.1 | drakonis.local |
| 120 | Serveurs | 10.120.0.0/16 | 10.120.4.0/24 | File server (10.120.4.1) | 10.120.0.1 | SMB |
| 120 | Serveurs | 10.120.0.0/16 | 10.120.5.0/24 | App services internes | 10.120.0.1 | Monitoring, jenkins... |
| 130 | VoIP | 10.130.0.0/24 | 10.130.0.0/24 | Téléphones IP (DHCP) | 10.130.0.1 | Trust IP phones only |
| 140 | IoT | 10.140.0.0/24 | 10.140.0.0/24 | Capteurs, imprimantes IoT | 10.140.0.1 | ⚠️ À CONFIRMER en équipe |
| 150 | Backup | 10.150.0.0/24 | 10.150.0.0/24 | Réplication out-of-band | 10.150.0.1 | ⚠️ Split-brain HSRP en cours |
| 999 | BlackHole | — | — | Native VLAN trunks (anti-VLAN hopping) | — | Aucune IP, anti-double-tagging |

## Transits inter-zones

| Transit | Réseau | IP pare-feu | IP R1 | IP R2 | Usage |
|---|---|---|---|---|---|
| pfSense externe ↔ Routeurs | 10.253.0.0/30 | 10.253.0.1 (pfSense externe) | 10.253.0.2 | 10.253.0.3 | Sortie Internet (NAT) |
| pfSense interne ↔ Routeurs | 10.254.0.0/30 | 10.254.0.1 (pfSense interne) | 10.254.0.2 | 10.254.0.3 | Filtrage inter-zones |

## Cloud AWS (eu-west-3 Paris)

VPC `172.16.0.0/16`, choisi pour éviter le conflit avec le VLAN 50 (`10.50.0.0/24`). RDS Multi-AZ, EC2 derrière ALB, ElastiCache, S3 avec Object Lock.

## Lecture d'une adresse

- **Principe général** : 10.[VLAN].[fonction].[host]/24
- **1er octet** : 10 — RFC1918 (privé)
- **2e octet** : Numéro du VLAN (10, 20, 30, 50, 100, 110, 120, 130, 140, 150)
- **3e octet** : Fonction ou sous-département dans le VLAN
- **4e octet** : Hôte (.1 = VIP HSRP, .2 = R1, .3 = R2, .10-.250 = hosts)

**Convention .1 .2 .3**

- **.0** : Network — non utilisé
- **.1** : Gateway HSRP virtuelle (VIP) — utilisée par les clients comme passerelle
- **.2** : Routeur R1 (Active, priorité HSRP 110, preempt)
- **.3** : Routeur R2 (Standby, priorité HSRP 100)
- **.10 → .250** : Pool hosts (statique ou DHCP)
- **.254** : VIP CARP des pfSense (sur VLAN 110 uniquement)
- **.255** : Broadcast — non utilisé

**Exemple lecture IP**

- **10.120.3.1** : VLAN 120 (serveurs), fonction 3 (AD/DNS), host .1 = DC1
- **10.110.1.254** : VLAN 110 (management), fonction 1 (firewalls), VIP CARP pfSense
- **10.10.1.50** : VLAN 10 (IT), fonction 1 (SysAdmins), host .50

**VLANs spéciaux**

- **VLAN 999 BlackHole** : Aucune IP. Utilisé comme native VLAN sur les trunks pour bloquer le double-tagging (anti-VLAN hopping).
- **VLAN 150 Backup** : Réplication backup out-of-band. Idéalement isolé du reste de l'infra (limite assumée : actuellement traverse les routeurs).

**Avantages de cette convention**

- **Lisibilité** : À la lecture d'une IP, on identifie immédiatement le VLAN et la fonction
- **Scalabilité** : Chaque VLAN /16 laisse 256 sous-réseaux /24 disponibles (jusqu'à 65k hosts par VLAN)
- **Audit** : Pour un auditeur, le schéma est auto-documenté
- **Filtrage** : Les ACL pfSense peuvent cibler des fonctions précises (ex : autoriser uniquement 10.120.3.0/24 vers DNS externe)
