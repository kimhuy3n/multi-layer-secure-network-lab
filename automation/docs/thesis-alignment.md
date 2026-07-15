# Thesis Alignment Notes

This note maps the graduation report to the repository layout so the GitHub project stays aligned with the written thesis.

## Report Summary

The thesis presents a multi-layer security architecture with:

- `pfSense` as firewall, gateway, and VPN endpoint
- `OpenVPN` for secure remote access
- `Snort IDS/IPS` for detection and prevention
- An Ubuntu-based SOC/monitoring host
- Python automation for analysis, response, and validation
- Grafana-based log review and incident visibility

## Architecture In The Report

```
Internet
  -> pfSense WAN
  -> pfSense LAN / Snort
  -> Internal LAN (Ubuntu Server)
  -> OpenVPN remote access for Kali / client machine
  -> SOC monitoring and incident response
```

## Reported Networks

- `WAN`: `172.20.10.0/24`
- `LAN`: `192.168.10.0/24`
- `OpenVPN`: `10.10.10.0/24`

## Main Experimental Scenarios

1. Firewall access control and segmentation
2. OpenVPN authentication and remote LAN access
3. Snort detection of:
   - ICMP ping
   - Nmap SYN scan
   - SSH and FTP authentication attempts
4. SOC monitoring of:
   - service port scans
   - SSH brute force
5. Incident response and IP blocking

## Repository Mapping

| Thesis component | Repository path | Status |
|---|---|---|
| Firewall planning | `automation/ansible/playbooks/03_firewall_rules.yml` | Documented and parameterized |
| Ubuntu hardening | `automation/ansible/playbooks/01_setup_ubuntu_server.yml` | Scripted |
| Snort layer | `automation/ansible/playbooks/02_setup_snort_ids.yml` | Documented with validation flow |
| SOC response | `automation/scripts/auto_response.py` | Prototype automation |
| Attack validation | `automation/scripts/attack_simulation.py` | Scripted |
| Test suite | `automation/scripts/test_all_layers.py` | Scripted |
| Monitoring stack | `automation/monitoring/docker-compose.yml` | Dockerized |

## What Is Already Represented Well

- Snort is part of the design and the validation flow.
- The network topology is represented in the extracted diagrams.
- The automation scripts are parameterized and safe to adjust with `.env`.

## What Still Depends On The Lab

- pfSense credentials and SSH access
- exact IP values in the live virtual machines
- log forwarding path from pfSense to syslog-ng
- whether Grafana shows live pfSense/Snort events in a given lab run

## Practical Reading Of The Repo

When presenting this project, describe the repository as:

- a thesis-aligned lab implementation
- a set of deployment and validation assets
- a monitoring and automation prototype that supports the written architecture

That framing is accurate to the report and avoids overclaiming beyond what the scripts currently automate.
