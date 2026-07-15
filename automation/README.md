# Automation Workflow

This folder contains the deployment and validation flow for the lab.

## Where Each Command Runs

- Control machine or Kali host: `Ansible`, Python validation scripts, attack simulation scripts
- Ubuntu monitoring host: Docker Compose stack for `syslog-ng`, `Promtail`, `Loki`, `Grafana`, and the SOC container
- pfSense: firewall rules, VPN, Snort, and block table

## Prerequisites

On the control machine:

```bash
sudo apt install ansible python3-pip sshpass -y
pip3 install -r scripts/requirements.txt
```

The Python scripts use `paramiko` and `requests`.

## Environment

Copy [`./.env.example`](./.env.example) to `./.env` and fill it with the values from your lab.

Important values:

- `PFSENSE_HOST`
- `PFSENSE_USER`
- `PFSENSE_PASS`
- `PFSENSE_URL`
- `PFSENSE_FW_LOG`
- `PFSENSE_SNORT_LOG`
- `PFSENSE_BLOCK_TABLE`
- `UBUNTU_HOST`
- `UBUNTU_USER`
- `UBUNTU_PASS`
- `VPN_GW`
- `LAB_SUBNET`
- `LAN_NETWORK`
- `LAN_GATEWAY`
- `VPN_NETWORK`
- `SNORT_TABLE`
- `INCIDENTS_LOG`

## Deployment Steps

### 1. Prepare the Ubuntu host

Run from the control machine:

```bash
cd automation
ansible-playbook -i ansible/inventory.ini ansible/playbooks/01_setup_ubuntu_server.yml
```

What it does:

- configures the internal Ubuntu server
- enables the hardening baseline
- prepares logging and service checks

### 2. Review Snort on pfSense

Run from the control machine:

```bash
cd automation
ansible-playbook -i ansible/inventory.ini ansible/playbooks/02_setup_snort_ids.yml
```

What it does:

- documents the Snort interface and rule flow
- checks the pfSense-side IDS/IPS setup
- keeps the lab notes aligned with the thesis

### 3. Review firewall rules

Run from the control machine:

```bash
cd automation
ansible-playbook -i ansible/inventory.ini ansible/playbooks/03_firewall_rules.yml
```

What it does:

- captures the WAN and LAN rule plan
- keeps the block/allow policy consistent with the report

### 4. Start the monitoring stack

Run on the Ubuntu monitoring host:

```bash
cd automation/monitoring
docker compose up -d
```

Expected containers:

- `syslog-ng`
- `Promtail`
- `Loki`
- `Grafana`
- `soc`

### 5. Run validation

Run from the control machine or Kali host:

```bash
cd automation/scripts
python3 test_all_layers.py
python3 attack_simulation.py
python3 auto_response.py
```

What to expect:

- `test_all_layers.py` reports pass/fail by layer
- `attack_simulation.py` triggers scan, brute-force, and flood scenarios
- `auto_response.py` reads logs and can block source IPs on pfSense

## Verification

Verify these items after the deploy:

- pfSense is reachable over SSH or WebGUI
- the OpenVPN network uses `10.10.10.0/24`
- Snort alerts appear in pfSense
- Ubuntu services are active
- Grafana shows incoming logs
- incident records are written to `automation/scripts/incidents.log`

## Troubleshooting

- If `VPN_GW` does not ping, confirm the OpenVPN tunnel is established and the gateway IP is correct.
- If Snort alerts are missing, locate the alert file on pfSense with:

```bash
find /var/log/snort -type f -name alert
```

- If IP blocking fails, confirm `PFSENSE_BLOCK_TABLE` matches the pfSense alias, for example `Blocked_IPs`.
- If Ansible fails, verify the inventory IPs and the `.env` credentials.
- If the monitoring stack is empty, check Docker container status and volume mounts on Ubuntu.

## Notes

- The default values are aligned with the thesis topology.
- If your lab uses different IPs or aliases, update `.env` instead of editing the scripts.
- The automation is designed for a lab environment, not production.
