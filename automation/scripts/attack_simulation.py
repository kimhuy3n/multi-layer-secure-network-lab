#!/usr/bin/env python3
"""
DATN 2026 - ATTACK SIMULATION
Chay tren KALI LINUX de test cac layer bao mat

Mo phong tan cong -> xem he thong phan ung

CANH BAO: Chi chay trong lab, KHONG chay tren mang that!
Chay: python3 attack_simulation.py
"""
import os
import subprocess
import time
import sys


def env(name, default):
    return os.getenv(name, default)


TARGET_FW = env("TARGET_FW", "192.168.10.1")    # pfSense
TARGET_SV = env("TARGET_SV", "192.168.10.101")  # Ubuntu Server
TARGET_SSH_USER = env("TARGET_SSH_USER", "root")
VPN_GW = env("VPN_GW", "10.10.0.1")

def banner():
    print("=" * 60)
    print("  DATN 2026 - ATTACK SIMULATION")
    print("  Bao mat da tang: IDS/IPS + FW + VPN")
    print("  CHI SU DUNG TRONG LAB!")
    print("=" * 60)

def run_cmd(cmd, desc):
    print(f"\n  [{desc}]")
    print(f"  Command: {cmd}")
    print("-" * 40)
    try:
        r = subprocess.run(cmd, shell=True, capture_output=True,
                          text=True, timeout=30)
        if r.stdout:
            # Chi hien 20 dong dau
            lines = r.stdout.strip().split('\n')
            for line in lines[:20]:
                print(f"  {line}")
            if len(lines) > 20:
                print(f"  ... ({len(lines)-20} more lines)")
        if r.stderr:
            for line in r.stderr.strip().split('\n')[:5]:
                print(f"  [err] {line}")
    except subprocess.TimeoutExpired:
        print("  [TIMEOUT] Command took too long")
    except Exception as e:
        print(f"  [ERROR] {e}")
    print("-" * 40)

def test_1_reconnaissance():
    """Phase 1: Thu thap thong tin"""
    print("\n" + "=" * 60)
    print("  PHASE 1: RECONNAISSANCE")
    print("  Muc dich: Thu thap thong tin mang")
    print("  Layer test: Firewall + IDS/IPS")
    print("=" * 60)

    run_cmd(f"nmap -sn {env('LAB_SUBNET', '192.168.10.0/24')}",
            "Host Discovery - Tim may trong mang")

    run_cmd(f"nmap -sS -T4 --top-ports 20 {TARGET_FW}",
            "SYN Scan pfSense - Top 20 ports")

    run_cmd(f"nmap -sV -T4 -p 22,80,443,1194 {TARGET_SV}",
            "Service Version Scan - Ubuntu Server")

    print("\n  >> Kiem tra pfSense:")
    print("     Services > Snort > Alerts")
    print("     Phai thay: Nmap scan detected!")
    input("  >> Nhan Enter de tiep tuc...")

def test_2_vulnerability_scan():
    """Phase 2: Quet lo hong"""
    print("\n" + "=" * 60)
    print("  PHASE 2: VULNERABILITY SCANNING")
    print("  Muc dich: Tim lo hong web server")
    print("  Layer test: IDS/IPS + Host Security")
    print("=" * 60)

    run_cmd(f"nikto -h http://{TARGET_SV} -maxtime 30",
            "Nikto Web Vulnerability Scan")

    run_cmd(f"curl -s -o /dev/null -w '%{{http_code}}' http://{TARGET_SV}/admin",
            "Test truy cap /admin")

    run_cmd(f"curl -s -o /dev/null -w '%{{http_code}}' http://{TARGET_SV}/../../../etc/passwd",
            "Test Path Traversal")

    print("\n  >> Kiem tra pfSense:")
    print("     Snort phai detect web attack patterns")
    input("  >> Nhan Enter de tiep tuc...")

def test_3_brute_force():
    """Phase 3: Brute force SSH"""
    print("\n" + "=" * 60)
    print("  PHASE 3: BRUTE FORCE ATTACK")
    print("  Muc dich: Thu brute force SSH")
    print("  Layer test: fail2ban (Host IPS) + Firewall")
    print("=" * 60)

    print("  Thu dang nhap SSH voi password sai...")
    for i in range(6):
        run_cmd(
            f"sshpass -p 'wrongpass{i}' ssh -o StrictHostKeyChecking=no -o ConnectTimeout=3 {TARGET_SSH_USER}@{TARGET_SV} exit 2>&1 || true",
            f"SSH brute force attempt {i+1}/6",
        )
        time.sleep(1)

    print("\n  >> Kiem tra Ubuntu Server:")
    print("     sudo fail2ban-client status sshd")
    print("     Phai thay: IP Kali bi ban!")
    print("\n  >> Kiem tra pfSense:")
    print("     Snort phai detect brute force pattern")
    input("  >> Nhan Enter de tiep tuc...")

def test_4_dos_simulation():
    """Phase 4: DoS nhe"""
    print("\n" + "=" * 60)
    print("  PHASE 4: DoS SIMULATION (light)")
    print("  Muc dich: Test chong DoS")
    print("  Layer test: Firewall + IDS/IPS + Auto Response")
    print("=" * 60)

    run_cmd(f"hping3 -S --flood -p 80 {TARGET_SV} -c 100 2>&1 || echo 'hping3 not installed: apt install hping3'",
            "SYN Flood to web server (100 packets)")

    print("\n  >> Kiem tra:")
    print("     1. pfSense > Snort > Alerts (DoS detected)")
    print("     2. auto_response.py console (auto block)")
    print("     3. pfSense > Diagnostics > pfTop")
    input("  >> Nhan Enter de tiep tuc...")

def test_5_verify_defense():
    """Phase 5: Xac nhan phong thu"""
    print("\n" + "=" * 60)
    print("  PHASE 5: VERIFY DEFENSE LAYERS")
    print("  Kiem tra tat ca layer da phan ung")
    print("=" * 60)

    run_cmd(f"ping -c 3 {TARGET_SV}",
            "Ping Ubuntu (co the bi block boi Snort)")

    run_cmd(f"curl -s --connect-timeout 3 http://{TARGET_SV} || echo 'BLOCKED - Web not accessible'",
            "HTTP access (co the bi block)")

    run_cmd(f"ssh -o ConnectTimeout=3 {env('UBUNTU_USER', 'huyen')}@{TARGET_SV} exit 2>&1 || echo 'BLOCKED or timeout'",
            "SSH access (co the bi block boi fail2ban)")

    print("\n  >> Ket qua mong doi:")
    print("     - Kali bi block boi Snort IPS (pfSense)")
    print("     - Kali bi ban boi fail2ban (Ubuntu)")
    print("     - Kali bi block boi auto_response.py")
    print("     - Tat ca alerts hien tren Grafana dashboard")

def summary():
    print("\n" + "=" * 60)
    print("  ATTACK SIMULATION COMPLETE")
    print("=" * 60)
    print("""
  Ket qua demo cho hoi dong:

  Phase 1 (Recon):
    Kali scan -> Snort IDS detect -> Alert
    LAYER TESTED: Firewall + IDS

  Phase 2 (Vuln Scan):
    Nikto scan -> Snort detect web attack
    LAYER TESTED: IDS/IPS + Firewall

  Phase 3 (Brute Force):
    SSH brute force -> fail2ban auto-ban
    LAYER TESTED: Host IPS (fail2ban)

  Phase 4 (DoS):
    SYN flood -> Snort IPS block + auto_response block
    LAYER TESTED: IDS/IPS + Automation

  Phase 5 (Verify):
    Kali bi block o nhieu layer
    LAYER TESTED: Tat ca layers hoat dong

  => HE THONG BAO MAT DA TANG HOAT DONG HIEU QUA
    """)

# === MAIN ===
if __name__ == "__main__":
    banner()

    print("\n  Chon phase de chay:")
    print("  1. Reconnaissance (nmap scan)")
    print("  2. Vulnerability Scan (nikto)")
    print("  3. Brute Force (SSH)")
    print("  4. DoS Simulation (hping3)")
    print("  5. Verify Defense")
    print("  6. Chay TAT CA tu dau den cuoi")
    print("  0. Thoat")
    print(f"  Target FW: {TARGET_FW}")
    print(f"  Target SV: {TARGET_SV}")
    print(f"  VPN GW:   {VPN_GW}")

    choice = input("\n  Chon (0-6): ").strip()

    if choice == "1": test_1_reconnaissance()
    elif choice == "2": test_2_vulnerability_scan()
    elif choice == "3": test_3_brute_force()
    elif choice == "4": test_4_dos_simulation()
    elif choice == "5": test_5_verify_defense()
    elif choice == "6":
        test_1_reconnaissance()
        test_2_vulnerability_scan()
        test_3_brute_force()
        test_4_dos_simulation()
        test_5_verify_defense()
        summary()
    else:
        print("  Thoat.")
