#!/usr/bin/env python3
"""
DATN 2026 - AUTO INCIDENT RESPONSE
Bao mat da tang: IDS/IPS + Firewall + VPN
Doc log pfSense + Snort -> Phat hien -> Tu dong block
"""
import os
import paramiko
import time
import re
import json
from datetime import datetime
from collections import defaultdict
from pathlib import Path

from runtime_config import env, load_env, SCRIPT_DIR

load_env()


# === CAU HINH ===
PFSENSE_HOST = env("PFSENSE_HOST", "192.168.10.1")
PFSENSE_USER = env("PFSENSE_USER", "admin")
PFSENSE_PASS = env("PFSENSE_PASS", "CHANGE_ME")
FW_LOG = env("PFSENSE_FW_LOG", "/var/log/filter.log")
SNORT_LOG = env("PFSENSE_SNORT_LOG", "/var/log/snort/alert")
AUTO_BLOCK_TABLE = env("PFSENSE_BLOCK_TABLE", "auto_blocked")
INCIDENTS_LOG = Path(env("INCIDENTS_LOG", str(SCRIPT_DIR / "incidents.log")))
PORTSCAN_THRESHOLD = int(env("PORTSCAN_THRESHOLD", "10"))
DOS_THRESHOLD = int(env("DOS_THRESHOLD", "500"))
CHECK_INTERVAL = int(env("CHECK_INTERVAL", "5"))
WHITELIST = [
    ip.strip()
    for ip in env(
        "WHITELIST",
        "192.168.10.1,192.168.10.101,192.168.10.102,10.10.0.1",
    ).split(",")
    if ip.strip()
]


class ThreatDetector:
    def __init__(self):
        self.conn_log = defaultdict(list)
        self.blocked = set()
        self.stats = {"events":0, "threats":0, "blocked":0}

    def check_portscan(self, src_ip, dst_port, ts):
        key = f"ps_{src_ip}"
        self.conn_log[key].append((ts, dst_port))
        recent = [(t,p) for t,p in self.conn_log[key] if t > ts-60]
        self.conn_log[key] = recent
        ports = len(set(str(p) for _,p in recent))
        if ports > PORTSCAN_THRESHOLD:
            self.stats["threats"] += 1
            return {"type":"PORT_SCAN","src_ip":src_ip,"severity":"HIGH",
                    "detail":f"{ports} ports in 60s","action":"BLOCK",
                    "timestamp":datetime.now().isoformat()}
        return None

    def check_dos(self, src_ip, ts):
        key = f"dos_{src_ip}"
        self.conn_log[key].append(ts)
        recent = [t for t in self.conn_log[key] if t > ts-10]
        self.conn_log[key] = recent
        if len(recent) > DOS_THRESHOLD:
            self.stats["threats"] += 1
            return {"type":"DOS_ATTACK","src_ip":src_ip,"severity":"CRITICAL",
                    "detail":f"{len(recent)} pkts in 10s","action":"BLOCK",
                    "timestamp":datetime.now().isoformat()}
        return None

    def check_snort(self, line):
        alert = re.search(r'\[\*\*\]\s+\[(\d+:\d+:\d+)\]\s+(.*?)\s+\[\*\*\]', line)
        ip = re.search(r'(\d+\.\d+\.\d+\.\d+):\d+\s+->\s+(\d+\.\d+\.\d+\.\d+)', line)
        pri = re.search(r'\[Priority:\s+(\d+)\]', line)
        if alert and ip:
            src = ip.group(1)
            if src in WHITELIST or src in self.blocked:
                return None
            p = int(pri.group(1)) if pri else 3
            sev = "CRITICAL" if p<=1 else "HIGH" if p<=2 else "MEDIUM"
            self.stats["threats"] += 1
            return {"type":"SNORT_ALERT","src_ip":src,"severity":sev,
                    "detail":alert.group(2),"action":"BLOCK" if p<=2 else "ALERT",
                    "timestamp":datetime.now().isoformat()}
        return None

    def analyze_fw(self, line):
        self.stats["events"] += 1
        parts = line.split(",")
        if len(parts) < 25:
            return []
        try:
            src_ip = parts[18]
            dst_port = parts[24]
        except IndexError:
            return []
        if not src_ip or src_ip in WHITELIST or src_ip in self.blocked:
            return []
        threats = []
        ts = time.time()
        t = self.check_portscan(src_ip, dst_port, ts)
        if t: threats.append(t)
        t = self.check_dos(src_ip, ts)
        if t: threats.append(t)
        return threats


class AutoResponder:
    def __init__(self):
        self.blocked = set()

    def respond(self, threat):
        ip = threat["src_ip"]
        if ip in self.blocked:
            return
        print(f"\n{'='*60}")
        print(f"  THREAT: {threat['type']}")
        print(f"  Source: {ip}")
        print(f"  Level:  {threat['severity']}")
        print(f"  Detail: {threat['detail']}")
        print(f"  Time:   {threat['timestamp']}")
        print(f"{'='*60}")

        if threat["action"] in ["BLOCK","BLOCK_IMMEDIATE"]:
            self._block(ip, threat)
        self._log(threat)

    def _block(self, ip, threat):
        print(f"  [ACTION] Blocking {ip} on pfSense...")
        try:
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect(PFSENSE_HOST, username=PFSENSE_USER,
                       password=PFSENSE_PASS, timeout=10,
                       allow_agent=False, look_for_keys=False)
            ssh.exec_command(f"pfctl -t {AUTO_BLOCK_TABLE} -T add {ip}")
            ts = datetime.now().isoformat()
            ssh.exec_command(f'echo "{ts} BLOCKED {ip} {threat["type"]}" >> /var/log/auto_response.log')
            ssh.close()
            self.blocked.add(ip)
            print(f"  [OK] {ip} BLOCKED (pfctl table: {AUTO_BLOCK_TABLE})")
        except Exception as e:
            print(f"  [ERROR] {e}")
            print(f"  [MANUAL] Block {ip} via pfSense WebGUI")

    def _log(self, threat):
        INCIDENTS_LOG.parent.mkdir(parents=True, exist_ok=True)
        with INCIDENTS_LOG.open("a", encoding="utf-8") as f:
            f.write(json.dumps(threat) + "\n")
        print(f"  [LOG] Saved to {INCIDENTS_LOG}")


class Monitor:
    def __init__(self):
        self.detector = ThreatDetector()
        self.responder = AutoResponder()

    def run(self):
        print("="*60)
        print("  DATN 2026 - AUTO INCIDENT RESPONSE")
        print("  Bao mat da tang: IDS/IPS + FW + VPN")
        print(f"  Target: {PFSENSE_HOST}")
        print(f"  Interval: {CHECK_INTERVAL}s")
        print("="*60)
        print("  Monitoring... (Ctrl+C to stop)\n")

        while True:
            try:
                ssh = paramiko.SSHClient()
                ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                ssh.connect(PFSENSE_HOST, username=PFSENSE_USER,
                           password=PFSENSE_PASS, timeout=10,
                           allow_agent=False, look_for_keys=False)

                # Read firewall log
                _,out,_ = ssh.exec_command(f"tail -50 {FW_LOG} 2>/dev/null")
                for line in out.readlines():
                    for t in self.detector.analyze_fw(line.strip()):
                        self.responder.respond(t)

                # Read Snort alerts
                _,out,_ = ssh.exec_command(f"tail -50 {SNORT_LOG} 2>/dev/null")
                for line in out.readlines():
                    t = self.detector.check_snort(line.strip())
                    if t:
                        self.responder.respond(t)

                ssh.close()
            except paramiko.AuthenticationException:
                print("[ERROR] SSH auth failed")
                print("[FIX] Enable SSH: pfSense > System > Advanced > Enable SSH")
                time.sleep(30)
            except Exception as e:
                print(f"[ERROR] {e}")
                time.sleep(10)

            time.sleep(CHECK_INTERVAL)


if __name__ == "__main__":
    try:
        Monitor().run()
    except KeyboardInterrupt:
        print(f"\nStopped. Check: {INCIDENTS_LOG}")
