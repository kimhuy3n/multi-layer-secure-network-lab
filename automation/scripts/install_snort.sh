#!/bin/bash
# DATN 2026 - Auto Install Snort on pfSense
# Run from vpn-client-01: ssh admin@192.168.10.1 < install_snort.sh

PFSENSE_HOST="${PFSENSE_HOST:-192.168.10.1}"
PFSENSE_USER="${PFSENSE_USER:-admin}"
PFSENSE_PASS="${PFSENSE_PASS:-CHANGE_ME}"

echo "=========================================="
echo "Snort Installation via SSH"
echo "=========================================="

SSH_BASE=(sshpass -p "$PFSENSE_PASS" ssh -o StrictHostKeyChecking=no "${PFSENSE_USER}@${PFSENSE_HOST}")
ssh_cmd() {
    "${SSH_BASE[@]}" "$@"
}

# Step 1: Install Snort package
echo "[1/5] Installing Snort package..."
ssh_cmd "pkg install -y snort"

# Step 2: Create rules directory
echo "[2/5] Creating rules directory..."
ssh_cmd "mkdir -p /var/db/snort/rules"

# Step 3: Download ET Open rules
echo "[3/5] Downloading ET Open rules..."
ssh_cmd "cd /var/db/snort/rules && fetch -o et.tar.gz https://rules.emergingthreats.net/open/snort-2.9/emerging.rules.tar.gz && tar -xzf et.tar.gz"

# Step 4: Start Snort
echo "[4/5] Starting Snort service..."
ssh_cmd "service snortd start"

# Step 5: Verify
echo "[5/5] Verifying Snort..."
ssh_cmd "ps aux | grep snort | grep -v grep"

echo "=========================================="
echo "Snort installation complete!"
echo "=========================================="
echo ""
echo "Next: Configure via WebGUI"
echo "  System > Package Manager"
echo "  Services > Snort > Interfaces"
echo "=========================================="
