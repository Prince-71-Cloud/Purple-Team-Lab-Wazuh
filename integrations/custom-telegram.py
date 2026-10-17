#!/usr/bin/env python3
"""
Wazuh -> Telegram custom integration.

Location on the MANAGER:
    /var/ossec/etc/rules/   -> no; this goes in:
    /var/ossec/integrations/custom-telegram.py

Wazuh's integrator daemon calls this script with three arguments:
    argv[1] = path to a JSON file containing ONE alert
    argv[2] = api_key   (from the <api_key> option, if set)
    argv[3] = hook_url  (from the <hook_url> option in ossec.conf)

For manual testing you can instead export TG_HOOK_URL and point the script at
the full alerts log (it reads the first line):
    sudo TG_HOOK_URL="https://api.telegram.org/bot<BOT_TOKEN>/sendMessage" \
      /var/ossec/integrations/custom-telegram /var/ossec/logs/alerts/alerts.json

SECURITY: keep your real CHAT_ID and bot token out of version control.
Leave the placeholders below in the published copy.
"""
import sys
import json
import os
import requests

# ---- CONFIG ----
CHAT_ID = "<TELEGRAM_CHAT_ID>"      # your numeric Telegram chat ID (from @userinfobot)
# ----------------


def main():
    alert_file = sys.argv[1]
    # Wazuh supplies the hook_url as argv[3]; fall back to env var for manual tests.
    hook_url = sys.argv[3] if len(sys.argv) > 3 else os.environ.get("TG_HOOK_URL", "")

    with open(alert_file, encoding="utf-8", errors="ignore") as f:
        content = f.read().strip()

    # Wazuh passes one alert; the alerts.json log holds many (one JSON per line).
    # Reading the first line makes the script work in both cases.
    first = content.splitlines()[0] if content else "{}"
    alert = json.loads(first)

    rule = alert.get("rule", {})
    agent = alert.get("agent", {})
    data = alert.get("data", {})

    level = rule.get("level", "N/A")
    rule_id = rule.get("id", "N/A")
    description = rule.get("description", "No description")
    agent_name = agent.get("name", "N/A")
    timestamp = alert.get("timestamp", "N/A")
    srcip = data.get("srcip", "")
    mitre_ids = rule.get("mitre", {}).get("id", [])

    # Severity emoji: red >= 12, orange >= 7, else green
    try:
        lvl = int(level)
    except (ValueError, TypeError):
        lvl = 0
    emoji = "\U0001F7E2"
    if lvl >= 12:
        emoji = "\U0001F534"
    elif lvl >= 7:
        emoji = "\U0001F7E0"

    lines = [
        f"{emoji} Wazuh Alert (level {level})",
        f"Rule: {rule_id} - {description}",
        f"Agent: {agent_name}",
    ]
    if srcip:
        lines.append(f"Source IP: {srcip}")
    if mitre_ids:
        lines.append(f"MITRE ATT&CK: {', '.join(mitre_ids)}")
    lines.append(f"Time: {timestamp}")

    # Plain text (no Markdown) so rule descriptions with _ or * always deliver.
    payload = {"chat_id": CHAT_ID, "text": "\n".join(lines)}
    requests.post(hook_url, json=payload, timeout=10)


if __name__ == "__main__":
    main()
