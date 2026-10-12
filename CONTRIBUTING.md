# Contributing

Thanks for your interest in improving this lab. This is primarily a learning/portfolio
project, but community rules, fixes, and ideas are very welcome.

## Ways to contribute

- **New detection rules** — custom Wazuh rules for attacks not yet covered (always in the
  `100000+` ID range).
- **Decoders** — decoders for log sources Wazuh doesn't parse out of the box.
- **Documentation** — clearer setup steps, fixes, or additional attack→detect walkthroughs.
- **Attack simulations** — reproducible, safe-to-run emulation commands.

## Ground rules

1. **No secrets.** Never commit real IP addresses, hostnames, passwords, tokens, or API
   keys. Use clearly marked placeholders such as `<MANAGER_IP>` or `<AGENT_IP>`.
2. **Lab safety.** Anything that emulates an attack must be intended for an **isolated lab**
   against machines the operator owns. Do not add content aimed at systems you don't control.
3. **Validate rules.** Run `sudo /var/ossec/bin/wazuh-logtest` and paste the matching output
   in your pull request so reviewers can see the rule fires as intended.
4. **Map to ATT&CK.** New detections should include a `<mitre>` block with the relevant
   technique ID.

## Pull request checklist

- [ ] No sensitive values committed (IPs, creds, tokens, hostnames)
- [ ] New rules use IDs `100000+`
- [ ] `wazuh-logtest` output included for any new rule
- [ ] ATT&CK technique referenced
- [ ] Docs updated if behavior or setup changed

## Reporting issues

Open an issue describing the problem, your Wazuh version, the OS of the manager/agent, and
the exact steps to reproduce. Screenshots of the relevant dashboard event help a lot.
