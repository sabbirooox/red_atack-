import requests
import socket
import sys
import time
import os
from urllib.parse import urlparse, parse_qs, urlencode, urlunparse

try:
    from colorama import Fore, Style, init
    init(autoreset=True)
except ImportError:
    os.system("pip install colorama requests")
    from colorama import Fore, Style, init
    init(autoreset=True)

target_url = "Not Set"

def clear_screen():
    os.system('clear' if os.name == 'posix' else 'cls')

def show_banner():
    clear_screen()
    print(Fore.RED + "==================================================")
    print(Fore.RED + Style.BRIGHT + "  ____  _____ ____      _  _____ _____ _  __")
    print(Fore.RED + Style.BRIGHT + " |  _ \| ____|  _ \    / \|_   _|_   _| |/ /")
    print(Fore.RED + Style.BRIGHT + " | |_) |  _| | | | |  / _ \ | |   | | | ' / ")
    print(Fore.RED + Style.BRIGHT + " |  _ <| |___| |_| | / ___ \| |   | | | . \ ")
    print(Fore.RED + Style.BRIGHT + " |_| \_\_____|____/ /_/   \_\_|   |_| |_|\_\\")
    print(Fore.RED + "==================================================")
    print(Fore.MAGENTA + Style.BRIGHT + "            DEVELOPER BY SABBIR ØX")
    print(Fore.RED + "==================================================")
    print("")

def show_menu():
    print(Fore.CYAN + f"[1] " + Fore.WHITE + f"TARGET WEBSITE (Current: {target_url})")
    print(Fore.CYAN + f"[2] " + Fore.WHITE + f"SERVER INFO (IP & Server Type)")
    print(Fore.CYAN + f"[3] " + Fore.WHITE + f"DIRECTORY FINDER (Hidden Panels)")
    print(Fore.CYAN + f"[4] " + Fore.WHITE + f"SQLi SCANNER")
    print(Fore.RED + f"[5] " + Fore.WHITE + f"EXIT")
    print(Fore.RED + "==================================================")

def get_server_info(url):
    print(Fore.YELLOW + f"\n[*] Analyzing {url}...")
    try:
        parsed = urlparse(url)
        domain = parsed.netloc
        ip = socket.gethostbyname(domain)
        print(Fore.GREEN + f"[+] Target IP: {ip}")
        
        response = requests.get(url, timeout=5)
        server = response.headers.get("Server", "Unknown")
        print(Fore.GREEN + f"[+] Server Header: {server}")
        
        print(Fore.CYAN + "\n[*] Checking Security Headers:")
        if "X-Frame-Options" in response.headers:
            print(Fore.GREEN + "  [+] X-Frame-Options: ENABLED")
        else:
            print(Fore.RED + "  [-] X-Frame-Options: MISSING")
            
        if "Strict-Transport-Security" in response.headers:
            print(Fore.GREEN + "  [+] HSTS: ENABLED")
        else:
            print(Fore.RED + "  [-] HSTS: MISSING")
            
    except Exception as e:
        print(Fore.RED + f"[!] Error: {e}")
    input(Fore.YELLOW + "\nPress Enter to return...")

def directory_finder(url):
    print(Fore.YELLOW + f"\n[*] Searching hidden directories on {url}...")
    paths = ["admin", "login", "backup", "config", "robots.txt", "dashboard"]
    found = False
    
    for path in paths:
        check_url = f"{url.rstrip('/')}/{path}"
        try:
            res = requests.get(check_url, timeout=3)
            if res.status_code == 200:
                print(Fore.GREEN + f"[+] FOUND: {check_url}")
                found = True
            elif res.status_code == 403:
                print(Fore.YELLOW + f"[!] PROTECTED: {check_url}")
        except:
            pass
            
    if not found:
        print(Fore.RED + "[-] No common directories found.")
    input(Fore.YELLOW + "\nPress Enter to return...")

def sqli_scanner(url):
    print(Fore.YELLOW + f"\n[*] Testing SQL Injection on {url}...")
    parsed = urlparse(url)
    params = parse_qs(parsed.query)
    
    if not params:
        print(Fore.RED + "[!] No parameters found. (Use URL like ?id=1)")
        input(Fore.YELLOW + "\nPress Enter to return...")
        return
        
    payload = "'"
    for param in params:
        mod_params = params.copy()
        mod_params[param] = [payload]
        new_query = urlencode(mod_params, doseq=True)
        new_url = urlunparse((parsed.scheme, parsed.netloc, parsed.path, parsed.params, new_query, parsed.fragment))
        
        try:
            res = requests.get(new_url, timeout=5)
            if res.status_code == 500 or "SQL syntax" in res.text or "mysql_fetch" in res.text:
                print(Fore.GREEN + f"[+] VULNERABLE: SQLi on '{param}' parameter!")
            else:
                print(Fore.RED + f"[-] '{param}' is safe.")
        except:
            print(Fore.RED + f"[!] Error on '{param}'.")
            
    input(Fore.YELLOW + "\nPress Enter to return...")

def main():
    global target_url
    while True:
        show_banner()
        show_menu()
        
        choice = input(Fore.YELLOW + "\nSelect an option: " + Fore.WHITE)
        
        if choice == '1':
            target_url = input(Fore.CYAN + "Enter Target URL (e.g., http://testphp.vulnweb.com): ").strip()
            if not target_url.startswith("http"):
                target_url = "http://" + target_url
        elif choice == '2':
            if target_url != "Not Set":
                get_server_info(target_url)
            else:
                print(Fore.RED + "[!] Set target first!")
                time.sleep(1)
        elif choice == '3':
            if target_url != "Not Set":
                directory_finder(target_url)
            else:
                print(Fore.RED + "[!] Set target first!")
                time.sleep(1)
        elif choice == '4':
            if target_url != "Not Set":
                sqli_scanner(target_url)
            else:
                print(Fore.RED + "[!] Set target first!")
                time.sleep(1)
        elif choice == '5':
            print(Fore.RED + "Exiting... Goodbye!")
            sys.exit()
        else:
            print(Fore.RED + "Invalid option!")
            time.sleep(1)

if __name__ == "__main__":
    main()
