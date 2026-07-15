# DATN 2026 - BAO MAT DA TANG + AUTOMATION

## BUOC 0: Chuan bi tren Kali
```
sudo apt install ansible python3-pip sshpass -y
pip3 install paramiko requests
```

## CAU HINH MOI TRUONG
Sao chep `automation/.env.example` thanh `.env` va dien gia tri that truoc khi chay script.

## BUOC 1: ansible-playbook -i ansible/inventory.ini ansible/playbooks/01_setup_ubuntu_server.yml
## BUOC 2: ansible-playbook -i ansible/inventory.ini ansible/playbooks/02_setup_snort_ids.yml
## BUOC 3: ansible-playbook -i ansible/inventory.ini ansible/playbooks/03_firewall_rules.yml
## BUOC 4: python3 scripts/auto_response.py
## BUOC 5: python3 scripts/test_all_layers.py
## BUOC 6: python3 scripts/attack_simulation.py
