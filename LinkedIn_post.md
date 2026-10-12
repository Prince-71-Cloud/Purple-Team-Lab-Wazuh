# LinkedIn share kit

> Fill in the `<PLACEHOLDER>` bits, attach 2–3 screenshots (agents active, the
> brute-force/web events, and your custom rule 100100 firing at level 12), and add your repo
> link.

---

## Short caption (one-liner for the image/post header)

> I built a purple-team detection lab with Wazuh — and went from triggering built-in alerts
> to writing my own. Here's what I learned. 👇

---

## LinkedIn post (concise version)

I spent some time building a **purple-team detection lab** with the open-source **Wazuh**
SIEM/XDR — not to "install a dashboard," but to practice the actual craft of detection
engineering. 🛡️

The setup (all in an isolated VMware lab):
• **Kali** running the Wazuh manager + indexer + dashboard, plus attacker tooling
• A **Linux agent** (Ubuntu) hosting a vulnerable web app (DVWA)
• A **Windows agent** for endpoint telemetry

The loop I practiced: **attack → see what the SIEM catches → read the raw event → write a
rule to close the gap → validate → verify.**

A few things that stuck with me:
🔹 **The agent collects, the manager decides.** I first wrote a detection rule on the agent
and got zero results — rules only run on the manager. One mistake, lesson learned for good.
🔹 **You can't detect what you don't collect.** Wazuh caught SSH brute force out of the box,
but saw nothing on web attacks until I explicitly added the web-server log.
🔹 **Specific beats loud.** I turned a generic level-6 "common web attack" into a custom
**level-12** detection that names the technique (MITRE **T1083**) and embeds the attacker's
IP in the alert.
🔹 **Validate before you ship.** `wazuh-logtest` let me confirm a rule fires correctly
*before* restarting the SIEM — a real production habit.

Coming from a red-team / offensive background, the most satisfying part was seeing how much
that experience accelerates building good *detections*. Purple teaming, for real.

Full write-up + the repo (rules, configs, setup, lessons): <REPO_LINK>

#CyberSecurity #DetectionEngineering #Wazuh #BlueTeam #PurpleTeam #SIEM #MITREATTACK #SOC #InfoSec

---

## Alt text for the screenshot (accessibility)

> Wazuh dashboard Events view showing a custom detection rule (ID 100100) firing at severity
> level 12 for a path-traversal attack targeting /etc/passwd, with the attacker's source IP
> shown in the alert description.
