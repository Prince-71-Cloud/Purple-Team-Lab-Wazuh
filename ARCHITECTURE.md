# Architecture

## Overview

The lab runs entirely inside VMware on a single isolated (NAT) network segment so that the
Wazuh manager and all agents can reach each other while staying off the real/home network.

```
            ┌────────────────────────────────────────────────┐
            │              Isolated VMware network            │
            │                   (NAT segment)                 │
            │                                                 │
   Attacker │   ┌──────────────┐        ┌──────────────────┐  │
   + SIEM   │   │  Kali Linux  │        │  Ubuntu Server   │  │
   host ────┼──▶│  Wazuh       │◀──────▶│  Wazuh Agent     │  │
            │   │  Manager     │  1514  │  + Apache/DVWA   │  │
            │   │  Indexer     │  1515  │  + MariaDB       │  │
            │   │  Dashboard   │        └──────────────────┘  │
            │   └──────┬───────┘                              │
            │          │               ┌──────────────────┐  │
            │          └──────────────▶│  Windows (VMware)│  │
            │                   1514   │  Wazuh Agent     │  │
            │                          └──────────────────┘  │
            └────────────────────────────────────────────────┘
```

## Data flow

1. **Agents collect** logs (Linux auth log, Apache access log, Windows events) and ship them
   to the manager over TCP **1514**. Enrollment happens over **1515**.
2. **The manager decodes and evaluates.** Each event passes through a *decoder* (which parses
   raw text into fields like `srcip` and `url`) and then the *ruleset* (which decides whether
   an alert fires and at what severity). **This is the key mental model: the agent collects,
   the manager decides.** Rules therefore live on the manager, never on the agent.
3. **The indexer stores** the resulting alerts; **the dashboard** presents them for threat
   hunting, events, and compliance views.

## Components

| Component | Role | Host (lab) |
|-----------|------|------------|
| Wazuh Manager | Decoders, rules, alerting | Kali |
| Wazuh Indexer | Alert storage/search | Kali (consolidated) |
| Wazuh Dashboard | Web UI | Kali (consolidated) |
| Wazuh Agent (Linux) | Auth + web-server telemetry | Ubuntu Server |
| Wazuh Agent (Windows) | Endpoint telemetry | Windows |
| DVWA (+ Apache, MariaDB, PHP) | Vulnerable web target | Ubuntu Server |
| Kali tooling (`hydra`, `curl`) | Attack emulation | Kali |

> **Production note:** consolidating the manager, indexer, and dashboard onto one host is a
> lab simplification. A production deployment separates these onto dedicated nodes and uses a
> multi-node indexer cluster.

## Key design choices

- **Reserved rule IDs (`100000+`)** for all custom rules, to avoid collisions with the
  built-in ruleset.
- **Explicit web-log collection** on the agent, because Wazuh does not monitor the Apache
  access log by default.
- **`wazuh-logtest` validation** before every manager restart, so a malformed rule file
  cannot take the SIEM offline.

## Detection pipeline (worked example)

```
 curl .../fi/?page=../../../../etc/passwd
          │
          ▼
 Apache access.log  (on agent)
          │ shipped 1514
          ▼
 Manager: decoder  = web-accesslog   → extracts srcip, url, protocol, id
          │
          ▼
 Manager: ruleset
     built-in  31104  "Common web attack"       (level 6)
     custom   100100  "Path traversal → /etc/passwd from <srcip>" (level 12)  ← wins
          │
          ▼
 Indexer → Dashboard alert (ATT&CK T1083, PCI DSS 6.5)
```
