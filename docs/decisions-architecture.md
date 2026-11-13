# Décisions d'architecture

Arbitrages tranchés en équipe avant la démonstration. Chaque ligne documente le problème, les options et le choix retenu.

| # | Sujet | Options | Décision |
|---|---|---|---|
| 1 | VLAN VoIP vs IoT — confusion sur 130 vs 140 | A) VoIP=130, IoT=140 (matrice initiale)<br>B) VoIP=130, pas d'IoT (J2 routeurs)<br>C) Ajouter IoT en VLAN 140 (proposé ici) | C — VoIP=130 (déjà configuré sur routeurs), ajouter IoT=140 si retenu. Décider en équipe si l'IoT est dans le scope. |
| 2 | NAS Backup : 10.120.1.0/24 ou 10.120.2.0/24 ? | A) 10.120.1.0/24 (matrice initiale, conflit avec Wazuh)<br>B) 10.120.2.0/24 (whiteboard) | B — Le whiteboard est correct, la matrice initiale avait une erreur, corrigée en v3. |
| 3 | AWS VPC : 10.50.0.0/16 ou 172.16.0.0/16 ? | A) 10.50/16 — Conflit avec VLAN 50 Guest WiFi<br>B) 172.16/16 — Pas de conflit | B — Aucun bénéfice à garder 10.50, risque de routage assuré. |
| 4 | VLAN 150 Backup isolé : maintien ou suppression ? | A) Garder mais investiguer split-brain HSRP<br>B) Supprimer (NAS dans VLAN 120 suffit)<br>C) Garder sans HSRP (limite assumée) | C — Acceptable pour POC. À documenter dans le GRC comme 'limite assumée — failover gateway VLAN 150 hors scope POC'. |
| 5 | VIP gateways : .1 ou .254 ? | A) .1 — Convention actuelle conf routeurs (HSRP)<br>B) .254 — Convention whiteboard pour pfSense CARP | Les DEUX coexistent : .1 = VIP HSRP des routeurs (par VLAN) / .254 = VIP CARP pfSense (uniquement VLAN 110). Bien distinguer en présentation. |
| 6 | Sortie internet : R1+R2 vers pfSense externe (10.253) ou pfSense interne (10.254) ? | A) pfSense externe = sortie Internet, pfSense interne = filtrage interne<br>B) pfSense interne = sortie Internet | A — confirmé en J2. pfSense externe a le WAN GNS3, pfSense interne ne fait que du filtrage. Route default routeurs via 10.253.0.1. |
