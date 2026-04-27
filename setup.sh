#!/usr/bin/env bash

# HermuXclaw-CORE | Autonomous Setup & Bootstrap
# This script prepares the digital environment for Sovereign Agent Operations.

echo "------------------------------------------------------------"
echo "🧠 INITIATING HERMUXCLAW-CORE BOOTSTRAP"
echo "------------------------------------------------------------"

# 1. Update & System Dependencies
echo "[*] Updating system packages..."
pkg update -y && pkg upgrade -y
pkg install -y git python curl wget termux-api jq

# 2. Python Environment
echo "[*] Installing Python dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

# 3. Ollama Installation Bridge
echo "[*] Preparing Ollama Environment..."
if ! command -v ollama &> /dev/null
then
    echo "[!] Ollama not detected."
    echo "[*] Recommended: Install via 'proot-distro install debian' or native community builds."
    echo "[*] Attempting to fetch Ollama installation helper..."
    # Placeholder for the user to see how to install it
    echo "To run Ollama on Termux: 
    1. pkg install proot-distro
    2. proot-distro install debian
    3. proot-distro login debian
    4. curl -fsSL https://ollama.com/install.sh | sh
    5. ollama serve &
    6. ollama pull qwen2.5-coder:0.5b"
else
    echo "[✓] Ollama detected. Pulling Qwen2.5-Coder (Local Brain)..."
    ollama pull qwen2.5-coder:0.5b
fi

# 4. Persistence Initialization
echo "[*] Initializing Knowledge Graph (SQLite)..."
python3 -c "import sys, os; sys.path.append(os.path.expanduser('~/hermuxclaw')); from storage.db import db; print('[✓] DB Ready')"

# 5. Deployment Confirmation
echo "------------------------------------------------------------"
echo "✅ BOOTSTRAP COMPLETE"
echo "------------------------------------------------------------"
echo "Command Center: http://localhost:8013"
echo "Launch with:    make dev"
echo "------------------------------------------------------------"
