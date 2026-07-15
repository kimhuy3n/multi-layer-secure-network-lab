# Multi-Layer Secure Network Lab

Defense-in-Depth lab for firewall, IDS/IPS, VPN, host hardening, automation, and monitoring.

## Network Diagrams

### Topology

![Network topology](docs/images/network-topology.png)

### Experimental deployment

![Experimental deployment](docs/images/experimental-deployment.png)

## What is included

- pfSense firewall and routing
- OpenVPN remote access
- Snort IDS/IPS guidance and validation flow
- Ubuntu server hardening with UFW, fail2ban, auditd
- Python-based auto-response prototype
- Log collection and dashboard stack with Loki, Promtail, Grafana, and syslog-ng
- Attack simulation scripts for lab validation

## Repository layout

- `automation/ansible/` - deployment playbooks and inventory
- `automation/scripts/` - Python and shell automation
- `automation/monitoring/` - logging and dashboard stack
- `Firewall_fw-edge-01/`, `UbuntuSV_srv-lan-01/`, `Ubuntu_vpn-client-01/`, `Kali/` - VM artifacts and notes

## Secrets and environment variables

This repo is configured to avoid hardcoded credentials in scripts.

Set these variables before running the automation:

- `PFSENSE_HOST`
- `PFSENSE_USER`
- `PFSENSE_PASS`
- `UBUNTU_HOST`
- `UBUNTU_USER`
- `UBUNTU_PASS`
- `VPN_GW`
- `TARGET_FW`
- `TARGET_SV`
- `TARGET_SSH_USER`
- `LAB_SUBNET`
- `INCIDENTS_LOG`

See `automation/.env.example` for a sample configuration.

## Notes

- VM images and snapshots are ignored by Git through `.gitignore`.
- The automation scripts are intended for the lab environment only.
- The report should describe the SOC/monitoring part as a prototype unless you add a fully implemented bot and backend.
