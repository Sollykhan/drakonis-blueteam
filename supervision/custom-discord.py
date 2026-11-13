#!/usr/bin/env python3
import json
import sys
import requests
from datetime import datetime

alert_file = sys.argv[1]

webhook_url = None
for arg in sys.argv[1:]:
    if isinstance(arg, str) and arg.startswith("https://discord.com/api/webhooks/"):
        webhook_url = arg
        break

if not webhook_url:
    sys.stderr.write(f"Discord webhook URL not found in args: {sys.argv}\n")
    sys.exit(1)

with open(alert_file) as f:
    alert = json.load(f)

rule = alert.get("rule", {})
agent = alert.get("agent", {})
data = alert.get("data", {})

level = rule.get("level", 0)
description = rule.get("description", "N/A")
rule_id = rule.get("id", "N/A")
groups = ", ".join(rule.get("groups", []))
agent_name = agent.get("name", "N/A")
agent_id = agent.get("id", "N/A")
src_ip = data.get("srcip", alert.get("srcip", "N/A"))
dst_ip = data.get("dstip", alert.get("dstip", "N/A"))
src_user = data.get("srcuser", alert.get("srcuser", "N/A"))
timestamp = alert.get("timestamp", datetime.utcnow().isoformat())
full_log = alert.get("full_log", "")[:1500]

if level >= 12:
    color = 15158332
    emoji = "🔴"
elif level >= 10:
    color = 15844367
    emoji = "🟠"
elif level >= 8:
    color = 16776960
    emoji = "🟡"
else:
    color = 3447003
    emoji = "🔵"

fields = [
    {"name": "Regle", "value": f"`{rule_id}` - {description}", "inline": False},
    {"name": "Agent", "value": f"`{agent_name}` (ID {agent_id})", "inline": True},
    {"name": "Niveau", "value": str(level), "inline": True},
]

if src_ip != "N/A":
    fields.append({"name": "IP Source", "value": f"`{src_ip}`", "inline": True})

if dst_ip != "N/A":
    fields.append({"name": "IP Dest", "value": f"`{dst_ip}`", "inline": True})

if src_user != "N/A":
    fields.append({"name": "User", "value": f"`{src_user}`", "inline": True})

if groups:
    fields.append({"name": "Groupes", "value": groups, "inline": False})

if full_log:
    fields.append({"name": "Log", "value": f"```{full_log}```", "inline": False})

payload = {
    "username": "Wazuh - Drakonis",
    "embeds": [{
        "title": f"{emoji} Alerte Wazuh - Niveau {level}",
        "color": color,
        "fields": fields,
        "footer": {"text": f"wazuh01-loc | {timestamp}"}
    }]
}

try:
    r = requests.post(webhook_url, json=payload, timeout=10)
    r.raise_for_status()
except requests.exceptions.RequestException as e:
    sys.stderr.write(f"Discord webhook failed: {e}\n")
    sys.exit(1)
