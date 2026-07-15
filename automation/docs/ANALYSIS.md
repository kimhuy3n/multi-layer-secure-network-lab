# PHAN TICH DE TAI: BAO MAT DA TANG - IDS/IPS + FIREWALL + VPN

## HIEN TRANG LAB

```
TANG (LAYER)         | CONG NGHE       | TRANG THAI
---------------------|-----------------|------------------
Layer 1: Firewall    | pfSense         | DONE (co ban)
Layer 2: VPN         | OpenVPN         | DONE
Layer 3: IDS/IPS     | Snort           | DONE (da validate)
Layer 4: Automation  | Ansible+Python  | PARTIAL
Layer 5: Monitoring  | Grafana/Log     | PARTIAL
```

## VAN DE LON NHAT

De tai la "Bao mat da tang IDS/IPS + FW + VPN"
Nhung phan can hoan thien nhat hien la automation va monitoring,
khong phai IDS/IPS.

## THU TU UU TIEN

1. Hoan thien Ansible tu dong cau hinh toan bo lab
2. Python auto-response: detect -> block
3. Ket noi log pfSense -> syslog-ng -> Loki -> Grafana
4. Tinh chinh dashboard va rule set
