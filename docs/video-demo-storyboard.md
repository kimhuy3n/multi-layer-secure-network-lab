# Video Demo Storyboard

This document is a demo script for a short HD presentation video of the graduation project.

## Goal

Show the defense-in-depth lab as a clean, believable system demo:

- firewall and segmentation
- VPN remote access
- Snort IDS/IPS detection
- host hardening
- monitoring and incident response

## Video Structure

### Scene 1: Title

Visual:

- Project title
- full-screen view of the network topology diagram

Narration:

- "This project presents a multi-layer secure network architecture based on the defense-in-depth model."

### Scene 2: Overall Architecture

Visual:

- show the `network-topology.png`
- highlight pfSense in the center
- highlight LAN, WAN, and OpenVPN segments

Narration:

- "The system is divided into WAN, LAN, and OpenVPN zones."
- "pfSense acts as the firewall, gateway, and VPN endpoint."

### Scene 3: Lab Nodes

Visual:

- show the virtual machines
- pfSense
- Ubuntu server
- VPN client
- Kali attacker

Narration:

- "The lab is deployed on four virtual machines."
- "Ubuntu is the protected internal host, while Kali is used for validation and attack simulation."

### Scene 4: Firewall Layer

Visual:

- pfSense WAN rules
- blocked ports: Telnet, SMB, RDP, FTP

Narration:

- "The firewall layer blocks dangerous services and keeps the default-deny posture."

### Scene 5: OpenVPN Layer

Visual:

- OpenVPN connection log
- VPN user list
- remote client reaching internal network

Narration:

- "Authorized users connect through OpenVPN to reach the internal LAN securely."

### Scene 6: Snort IDS/IPS

Visual:

- Snort alerts
- nmap scan alert
- ICMP block alert

Narration:

- "Snort detects reconnaissance, scanning, and unauthorized traffic."
- "In IPS mode, selected traffic is blocked automatically."

### Scene 7: Host Hardening

Visual:

- Ubuntu hardening checklist
- fail2ban
- UFW
- auditd

Narration:

- "The Ubuntu host is hardened with fail2ban, UFW, auditd, and SSH restrictions."

### Scene 8: Monitoring and Response

Visual:

- Grafana dashboard
- Loki logs
- syslog-ng receiver
- auto-response console

Narration:

- "Logs are centralized and visualized for incident review."
- "The Python-based response module reads events and can block suspicious IPs."

### Scene 9: Attack Simulation

Visual:

- nmap scan
- SSH brute-force attempts
- light DoS/flood test

Narration:

- "The validation scenarios include scanning, brute force, and flood-style traffic."
- "Each attack is checked against the firewall, IDS/IPS, and host defenses."

### Scene 10: Conclusion

Visual:

- final topology view
- results summary

Narration:

- "The project demonstrates that layered security improves detection, prevention, and response in a controlled lab environment."

## Suggested Shot List

1. title screen
2. network topology diagram
3. pfSense VM and lab topology
4. firewall rules
5. OpenVPN logs and client access
6. Snort alerts
7. Ubuntu hardening commands or terminal output
8. Grafana dashboard and log flow
9. attack simulation screen recordings
10. closing slide with project summary

## Suggested Runtime

- 90 to 150 seconds for a CV-friendly version
- 3 to 5 minutes for a thesis presentation version

## Suggested On-Screen Text

- "Defense-in-Depth Security Lab"
- "Firewall"
- "OpenVPN"
- "Snort IDS/IPS"
- "Host Hardening"
- "Monitoring and Incident Response"
- "Attack Validation"

