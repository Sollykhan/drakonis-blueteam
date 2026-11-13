# Alerting Wazuh → Discord

Intégration développée de zéro pour Drakonis : chaque alerte Wazuh de **niveau 8 ou plus** est envoyée dans un salon Discord sous forme d'embed coloré selon la gravité.

| Fichier | Rôle |
|---|---|
| `custom-discord` | Lanceur shell : exécute le script avec le Python embarqué de Wazuh (`/var/ossec/framework/python`) |
| `custom-discord.py` | Lit l'alerte JSON, construit l'embed (règle, agent, niveau, IP source/destination, utilisateur, groupes, extrait du log) et le poste sur le webhook |
| `ossec-integration.xml` | Bloc `<integration>` à ajouter dans `ossec.conf` |

## Fonctionnement

1. Le manager Wazuh déclenche l'intégration pour chaque alerte dont le niveau est ≥ 8 (seuil choisi pour couper le bruit, notamment les résultats SCA de bas niveau).
2. Wazuh appelle `custom-discord` avec le chemin du fichier d'alerte et l'URL du webhook en arguments.
3. Le script **cherche l'URL parmi tous les arguments** au lieu de supposer sa position : c'est la correction du bug de lecture des arguments rencontré pendant le projet (l'ordre de `sys.argv` ne correspondait pas à ce qu'attendait la première version).
4. Code couleur : 🔴 ≥ 12 · 🟠 ≥ 10 · 🟡 ≥ 8. Le log brut est tronqué à 1 500 caractères pour respecter les limites de Discord.

## Installation

```bash
sudo cp custom-discord custom-discord.py /var/ossec/integrations/
sudo chown root:wazuh /var/ossec/integrations/custom-discord*
sudo chmod 750 /var/ossec/integrations/custom-discord*
# ajouter le bloc de ossec-integration.xml dans /var/ossec/etc/ossec.conf
sudo systemctl restart wazuh-manager
```

## Tester sans attaque réelle

```bash
logger -t sshd "Failed password for invalid user test from 10.10.1.50 port 4242 ssh2"   # répéter pour franchir le seuil
tail -f /var/ossec/logs/integrations.log
```

> **Sécurité :** l'URL d'un webhook Discord est un secret (quiconque la connaît peut poster dans le salon). Elle ne doit jamais être versionnée : Wazuh la passe en argument, elle n'apparaît pas dans le script.
