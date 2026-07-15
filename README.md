# Multi-Layer Secure Network Lab

Defense-in-Depth laboratory for a segmented network built around pfSense, OpenVPN, Snort, Ubuntu hardening, automation, and log monitoring.

## Overview

This project demonstrates a layered security architecture for a small virtual enterprise network. The lab is designed to show how preventive, detective, and responsive controls work together:

- `pfSense` provides firewalling, gateway routing, and VPN termination
- `Snort` is used as the IDS/IPS layer for scanning and attack detection
- `OpenVPN` provides authenticated remote access to the internal LAN
- `Ubuntu Server` is hardened with `UFW`, `fail2ban`, `auditd`, and logging
- Python scripts provide validation, incident response, and attack simulation
- A monitoring stack collects and visualizes logs for incident review

## Network Diagrams

### Topology

![Network topology](docs/images/network-topology.png)

### Experimental deployment

![Experimental deployment](docs/images/experimental-deployment.png)

## Lab Nodes

- `fw-edge-01` - pfSense firewall, gateway, VPN server
- `srv-lan-01` - internal Ubuntu server and monitoring host
- `vpn-client-01` - internal VPN client machine
- `kali-linux` - attacker/test machine for validation scenarios

## Key Capabilities

- Firewall rule planning for WAN and LAN traffic
- OpenVPN remote access with client certificate flow
- Snort IDS/IPS setup guide and validation checks
- Ubuntu host hardening with SSH restrictions and UFW policy
- Auto-response prototype that reads logs and attempts IP blocking
- Attack simulation workflow for reconnaissance, vulnerability checks, brute force, and DoS-style tests
- Log collection stack using Loki, Promtail, Grafana, and syslog-ng

## Repository Layout

- `automation/ansible/` - inventory, group vars, and playbooks
- `automation/scripts/` - Python and shell automation
- `automation/monitoring/` - logging and dashboard stack
- `docs/images/` - diagrams extracted from the report
- `Firewall_fw-edge-01/`, `UbuntuSV_srv-lan-01/`, `Ubuntu_vpn-client-01/`, `Kali/` - VM artifacts and local notes

## How To Use

1. Copy `automation/.env.example` to `.env`.
2. Fill in the environment values for your lab.
3. Run the Ansible playbooks or Python scripts from the `automation` folder.
4. Use the attack simulation script to validate firewall, IDS/IPS, VPN, and host security controls.

## Environment Variables

The scripts avoid hardcoded secrets and should be configured with environment variables.

Required or commonly used variables:

- `PFSENSE_HOST`
- `PFSENSE_USER`
- `PFSENSE_PASS`
- `PFSENSE_URL`
- `UBUNTU_HOST`
- `UBUNTU_USER`
- `UBUNTU_PASS`
- `VPN_GW`
- `TARGET_FW`
- `TARGET_SV`
- `TARGET_SSH_USER`
- `LAB_SUBNET`
- `LAN_NETWORK`
- `LAN_GATEWAY`
- `VPN_NETWORK`
- `VPN_PORT`
- `SNORT_TABLE`
- `PFSENSE_FW_LOG`
- `PFSENSE_SNORT_LOG`
- `PFSENSE_BLOCK_TABLE`
- `INCIDENTS_LOG`

See [`automation/.env.example`](automation/.env.example) for a sample configuration.

## Security Notes

- VM images, snapshots, logs, and office notes are ignored through `.gitignore`.
- The automation is intended for the lab environment only.
- The SOC/monitoring layer in the repository should be treated as a prototype unless you extend it with a full Telegram/SIEM backend.

## Report Traceability

The images in `docs/images/` were extracted from the project report so the GitHub repository matches the written thesis and shows the same topology and deployment model.
