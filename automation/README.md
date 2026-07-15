# Automation Workflow

This folder contains the deployment and validation workflow for the graduation project.

## 1. Prepare the control machine

On the control machine or Kali test host:

```bash
sudo apt install ansible python3-pip sshpass -y
pip3 install -r scripts/requirements.txt
```

## 2. Configure the environment

Copy [`automation/.env.example`](./.env.example) to `.env` and fill in the values for your lab.

The scripts read configuration from environment variables so the same code can be reused across lab instances.

## 3. Deploy the Ubuntu hardening layer

```bash
ansible-playbook -i ansible/inventory.ini ansible/playbooks/01_setup_ubuntu_server.yml
```

This playbook configures:

- Apache web service
- `fail2ban`
- `UFW`
- `auditd`
- SSH root login hardening
- syslog forwarding

## 4. Review the Snort IDS/IPS layer

```bash
ansible-playbook -i ansible/inventory.ini ansible/playbooks/02_setup_snort_ids.yml
```

This playbook documents the Snort installation and configuration flow described in the thesis:

- pfSense access check
- Snort package and interface setup
- rules category selection
- IDS/IPS validation steps

## 5. Review firewall rules

```bash
ansible-playbook -i ansible/inventory.ini ansible/playbooks/03_firewall_rules.yml
```

This playbook captures the pfSense WAN and LAN rule plan used in the thesis:

- block Telnet, SMB, RDP, and FTP on WAN
- allow only required LAN traffic
- keep the default deny posture

## 6. Start the monitoring stack

On the Ubuntu monitoring host:

```bash
cd monitoring
docker compose up -d
```

The stack includes:

- `Loki`
- `Grafana`
- `Promtail`
- `syslog-ng`
- `soc` Python container

## 7. Run validation

```bash
python3 scripts/test_all_layers.py
python3 scripts/attack_simulation.py
python3 scripts/auto_response.py
```

Expected validation flow:

- port scan triggers IDS/IPS alerts
- failed login attempts trigger host protection
- log events are stored for review
- incident response can block source IPs through the pfSense table

## 8. Environment variables

The main values used by the automation are listed in `.env.example`.

Important ones:

- `PFSENSE_HOST`
- `PFSENSE_USER`
- `PFSENSE_PASS`
- `PFSENSE_FW_LOG`
- `PFSENSE_SNORT_LOG`
- `PFSENSE_BLOCK_TABLE`
- `UBUNTU_HOST`
- `UBUNTU_USER`
- `UBUNTU_PASS`
- `VPN_GW`
- `LAB_SUBNET`
- `INCIDENTS_LOG`
