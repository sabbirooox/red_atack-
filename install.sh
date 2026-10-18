#!/bin/bash
clear
echo -e "\e[1;32m[+] Installing Requirements...\e[0m"
pkg update -y && pkg upgrade -y
pkg install python -y
pip install colorama requests

echo -e "\e[1;32m[+] Downloading RED ATACK Tool...\e[0m"
curl -sL https://raw.githubusercontent.com/sabbirooox/red_atack-/main/red_atack.py -o red_atack.py -o red_atack.py

chmod +x red_atack.py

echo -e "\e[1;34m[✓] Installation Complete!\e[0m"
echo -e "\e[1;33mType 'python red_atack.py' to run the tool.\e[0m"
