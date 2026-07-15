#!/usr/bin/env python3
"""
DATN 2026 - TEST SUITE
Kiem tra tat ca cac layer bao mat da tang
IDS/IPS + Firewall + VPN

Chay: python3 test_all_layers.py
"""
import os
import subprocess
import socket
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent


def env(name, default):
    return os.getenv(name, default)


# === CAU HINH ===
PFSENSE = env("PFSENSE_HOST", "192.168.10.1")
UBUNTU = env("UBUNTU_HOST", "192.168.10.101")
DNS = env("DNS_SERVER", "8.8.8.8")
VPN_GW = env("VPN_GW", "10.10.0.1")
PFSENSE_USER = env("PFSENSE_USER", "admin")
PFSENSE_PASS = env("PFSENSE_PASS", "CHANGE_ME")
UBUNTU_USER = env("UBUNTU_USER", "huyen")
UBUNTU_PASS = env("UBUNTU_PASS", "CHANGE_ME")
SNORT_TABLE = env("SNORT_TABLE", "snort2c")
INCIDENTS_LOG = Path(env("INCIDENTS_LOG", str(SCRIPT_DIR / "incidents.log")))

PASS = 0
FAIL = 0

def test(name, condition, detail=""):
    global PASS, FAIL
    if condition:
        PASS += 1
        print(f"  [PASS] {name}")
    else:
        FAIL += 1
        print(f"  [FAIL] {name} -- {detail}")

def ping(host, timeout=2):
    """Ping 1 host, return True/False"""
    try:
        param = "-n" if sys.platform == "win32" else "-c"
        timeout_param = "-w" if sys.platform == "win32" else "-W"
        timeout_val = str(timeout * 1000) if sys.platform == "win32" else str(timeout)
        r = subprocess.run(
            ["ping", param, "1", timeout_param, timeout_val, host],
            capture_output=True, text=True, timeout=timeout+2
        )
        return r.returncode == 0
    except:
        return False

def port_open(host, port, timeout=2):
    """Check 1 port co mo khong"""
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(timeout)
        result = s.connect_ex((host, port))
        s.close()
        return result == 0
    except:
        return False

def port_closed(host, port, timeout=2):
    return not port_open(host, port, timeout)


# ============================================================
print("=" * 60)
print("  DATN 2026 - MULTI-LAYER SECURITY TEST SUITE")
print("  Bao mat da tang: IDS/IPS + Firewall + VPN")
print("=" * 60)

# === LAYER 1: NETWORK CONNECTIVITY ===
print("\n--- LAYER 0: Network Connectivity ---")
test("Ping pfSense gateway",     ping(PFSENSE))
test("Ping Ubuntu Server",       ping(UBUNTU))
test("Ping Internet (DNS)",      ping(DNS))

# === LAYER 1: FIREWALL RULES ===
print("\n--- LAYER 1: Firewall (pfSense) ---")
test("pfSense WebGUI (443) open",     port_open(PFSENSE, 443))
test("VPN port (1194) accessible",    port_open(PFSENSE, 1194))
test("Telnet (23) BLOCKED",           port_closed(PFSENSE, 23), "Port 23 should be blocked!")
test("SMB (445) BLOCKED",             port_closed(PFSENSE, 445), "Port 445 should be blocked!")
test("RDP (3389) BLOCKED",            port_closed(PFSENSE, 3389), "Port 3389 should be blocked!")
test("FTP (21) BLOCKED",              port_closed(PFSENSE, 21), "Port 21 should be blocked!")

# === LAYER 2: IDS/IPS (Snort) ===
print("\n--- LAYER 2: IDS/IPS (Snort on pfSense) ---")
# Snort check: try to connect to pfSense and check Snort status
try:
    import paramiko
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(PFSENSE, username=PFSENSE_USER, password=PFSENSE_PASS,
                timeout=5, allow_agent=False, look_for_keys=False)
    _, out, _ = ssh.exec_command("pgrep -x snort 2>/dev/null")
    snort_pid = out.read().decode().strip()
    test("Snort process running", bool(snort_pid), "Snort not running - install via Package Manager")

    _, out, _ = ssh.exec_command(f"pfctl -t {SNORT_TABLE} -T show 2>/dev/null")
    snort_table = out.read().decode().strip()
    exit_status = out.channel.recv_exit_status()
    test("Snort block table exists", exit_status == 0, f"Table {SNORT_TABLE} not found")

    _, out, _ = ssh.exec_command("ls /var/log/snort/ 2>/dev/null | head -5")
    snort_logs = out.read().decode().strip()
    test("Snort log directory exists", bool(snort_logs), "No Snort logs found")

    ssh.close()
except ImportError:
    print("  [SKIP] paramiko not installed - pip3 install paramiko")
except Exception as e:
    test("SSH to pfSense", False, str(e))
    print("  [HINT] Enable SSH: System > Advanced > Admin Access > Enable SSH")

# === LAYER 3: VPN ===
print("\n--- LAYER 3: VPN (OpenVPN) ---")
test("VPN port 1194 reachable", port_open(PFSENSE, 1194))
test("VPN tunnel gateway ping",  ping(VPN_GW),
     "VPN not connected - run: sudo openvpn --config client.ovpn")

# === LAYER 4: HOST SECURITY (Ubuntu Server) ===
print("\n--- LAYER 4: Host Security (srv-lan-01) ---")
test("Ubuntu SSH (22) open",         port_open(UBUNTU, 22))
test("Ubuntu Web (80) open",         port_open(UBUNTU, 80))

try:
    import paramiko
    # Test SSH root disabled
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        ssh.connect(UBUNTU, username="root", password="root",
                    timeout=3, allow_agent=False, look_for_keys=False)
        test("Root SSH DISABLED", False, "ROOT LOGIN IS ALLOWED!")
        ssh.close()
    except paramiko.AuthenticationException:
        test("Root SSH DISABLED", True)
    except Exception as e:
        test("Root SSH DISABLED", False, f"Unexpected error: {e}")

    # Test services running
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(UBUNTU, username=UBUNTU_USER, password=UBUNTU_PASS,
                timeout=5, allow_agent=False, look_for_keys=False)

    _, out, _ = ssh.exec_command("systemctl is-active fail2ban 2>/dev/null")
    f2b = out.read().decode().strip()
    test("fail2ban running", f2b == "active", f"Status: {f2b}")

    _, out, _ = ssh.exec_command("ufw status 2>/dev/null | head -1")
    ufw = out.read().decode().strip()
    test("UFW firewall active", "active" in ufw.lower(), f"Status: {ufw}")

    _, out, _ = ssh.exec_command("systemctl is-active apache2 2>/dev/null")
    apache = out.read().decode().strip()
    test("Apache web server running", apache == "active", f"Status: {apache}")

    _, out, _ = ssh.exec_command("systemctl is-active auditd 2>/dev/null")
    audit = out.read().decode().strip()
    test("Audit daemon running", audit == "active", f"Status: {audit}")

    ssh.close()
except ImportError:
    print("  [SKIP] Install paramiko: pip3 install paramiko")
except Exception as e:
    print(f"  [ERROR] {e}")

# === LAYER 5: AUTO RESPONSE ===
print("\n--- LAYER 5: Automation ---")
test("auto_response.py exists",
     (SCRIPT_DIR / "auto_response.py").exists(),
     "Script not found")
test("incidents.log accessible",
     INCIDENTS_LOG.parent.exists(),
     f"Path not available: {INCIDENTS_LOG}")

# === SUMMARY ===
print("\n" + "=" * 60)
total = PASS + FAIL
print(f"  RESULTS: {PASS}/{total} passed, {FAIL} failed")
print(f"  Score:   {PASS/total*100:.0f}%" if total > 0 else "  No tests run")
print()

if FAIL == 0:
    print("  ALL LAYERS OPERATIONAL")
    print("  He thong bao mat da tang hoat dong tot!")
else:
    print("  SOME LAYERS NEED ATTENTION")
    print("  Kiem tra cac muc FAIL phia tren")

print()
print("  Layers tested:")
print("    [1] Firewall (pfSense rules)")
print("    [2] IDS/IPS (Snort)")
print("    [3] VPN (OpenVPN)")
print("    [4] Host Security (fail2ban + UFW)")
print("    [5] Automation (auto_response)")
print("=" * 60)
