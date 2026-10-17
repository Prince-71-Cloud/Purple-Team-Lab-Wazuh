# Real-time Telegram alerting

This integration pushes Wazuh alerts to a Telegram bot in real time, so high-severity
detections reach your phone the moment they fire. It runs on the **manager** via Wazuh's
`wazuh-integratord` daemon: when an alert crosses a severity threshold, the daemon executes a
custom script that POSTs the alert to the Telegram API.

> **Mental model:** the bot **token** authenticates the sender; the **chat ID** is the
> delivery address. Both are required for a message to arrive.

## Files

| File | Location on the manager | Purpose |
|------|-------------------------|---------|
| `custom-telegram.py` | `/var/ossec/integrations/custom-telegram.py` | Parses the alert JSON and sends the Telegram message |
| `custom-telegram` | `/var/ossec/integrations/custom-telegram` | Wrapper the integrator calls; runs the `.py` with Wazuh's bundled Python |
| `ossec-integration-snippet.xml` | inside `/var/ossec/etc/ossec.conf` | Registers the integration and sets the severity threshold |

## Setup

1. **Create a bot** with [@BotFather](https://t.me/BotFather) (`/newbot`) and copy the **bot token**.
2. **Get your chat ID**: message [@userinfobot](https://t.me/userinfobot) (press Start); it
   replies with your numeric `Id`. (A personal chat ID is a positive number with no leading
   zero — it is *not* your phone number.)
3. **Send your bot a message first** (open it, press Start, type anything). A bot cannot
   message a chat that has never messaged it.
4. Copy the two scripts into `/var/ossec/integrations/`, set your `CHAT_ID` in the `.py`, then:
   ```bash
   sudo chown root:wazuh /var/ossec/integrations/custom-telegram*
   sudo chmod 750 /var/ossec/integrations/custom-telegram*
   ```
5. Point the wrapper at the Python interpreter that exists on your manager
   (`ls /var/ossec/*/bin/python3` to find it — commonly
   `/var/ossec/framework/python/bin/python3` or `/var/ossec/venv/bin/python3`).
6. Add the `<integration>` block (see `ossec-integration-snippet.xml`) to `ossec.conf` with
   your token, then restart:
   ```bash
   sudo systemctl restart wazuh-manager
   ```

## Test

Manual (no attack needed):
```bash
sudo TG_HOOK_URL="https://api.telegram.org/bot<BOT_TOKEN>/sendMessage" \
  /var/ossec/integrations/custom-telegram /var/ossec/logs/alerts/alerts.json
```

Live (end-to-end) — brute force is level 10, so it crosses the threshold:
```bash
hydra -l fakeuser -P /usr/share/wordlists/rockyou.txt ssh://<AGENT_IP> -t 4
```

## Result

Live alerts delivered to the bot during an SSH brute force against the Ubuntu agent —
correlated rules **5712** (sshd brute force), **5551** (PAM multiple failed logins), and
**2502** (repeated password failures), all level 10 and mapped to **MITRE T1110**. Source IP
and bot username redacted.

![Telegram live alerts](../docs/screenshots/redacted/09-telegram-live-alerts.png)

## Troubleshooting

- **No message, no error:** wrong chat ID, or you haven't messaged the bot yet.
- **`python3: not found`:** the wrapper points at an interpreter path that doesn't exist on
  your build — fix it (step 5).
- **`ModuleNotFoundError: requests`:** you're using a Python without `requests`; either use
  Wazuh's bundled interpreter or `sudo <that-python> -m pip install requests`.
- **Nothing in the live test but the manual test works:** confirm the `<integration>` block is
  present and the manager was restarted; check `/var/ossec/logs/integrations.log`.
- For verbose logs, set `integrator.debug=2` in `/var/ossec/etc/internal_options.conf` and
  restart the manager.

## Security

The bot token and chat ID are credentials for *your* notifications. Keep the real
`ossec.conf` and the populated `custom-telegram.py` out of version control — the published
copies here use `<BOT_TOKEN>` and `<TELEGRAM_CHAT_ID>` placeholders.
