# Screenshots

Add your own exported dashboard screenshots here and reference them from the main README and
the learning summary. Suggested shots (all from **Threat Hunting → Events**, filtered):

| Suggested filename | What to capture | Filter |
|--------------------|-----------------|--------|
| `01-agents-active.png` | Agents list showing Linux + Windows agents **Active** | — |
| `02-ssh-bruteforce-5712.png` | SSH brute-force events | `rule.id:5712` |
| `03-web-attack-31104.png` | Built-in web attack detection | `rule.id:31104` |
| `04-web-attack-event-detail.png` | Expanded event: `srcip`, `url`, `rule.mitre.id`, compliance tags | `rule.id:31104` |
| `05-custom-rule-100100.png` | Your custom level-12 detection firing | `rule.id:100100` |
| `06-logtest-output.png` | `wazuh-logtest` showing rule 100100 matching at level 12 | — |

> Tip: crop out any real IPs/hostnames or blur them before publishing.
