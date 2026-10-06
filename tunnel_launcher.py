"""
SafeRide Public HTTPS Tunnel Launcher
Provides free, secure, instant public HTTPS tunnel for mobile WhatsApp live tracking.
Uses high-performance Cloudflare Tunnel (cloudflared.exe) or OpenSSH fallback.
"""

import os
import re
import sys
import time
import subprocess
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
TUNNEL_URL_FILE = BASE_DIR / '.tunnel_url'
ENV_FILE = BASE_DIR / '.env'
CLOUDFLARED_EXE = BASE_DIR / 'cloudflared.exe'

def update_env_file(public_url):
    """Saves the current public URL into .env and .tunnel_url"""
    try:
        with open(TUNNEL_URL_FILE, 'w', encoding='utf-8') as f:
            f.write(public_url.strip() + '\n')
    except Exception as e:
        print(f"[!] Could not write .tunnel_url: {e}")

    if ENV_FILE.exists():
        try:
            with open(ENV_FILE, 'r', encoding='utf-8') as f:
                content = f.read()

            if 'PUBLIC_TUNNEL_URL=' in content:
                content = re.sub(r'PUBLIC_TUNNEL_URL=.*', f'PUBLIC_TUNNEL_URL={public_url}', content)
            else:
                content += f"\nPUBLIC_TUNNEL_URL={public_url}\n"

            with open(ENV_FILE, 'w', encoding='utf-8') as f:
                f.write(content)
        except Exception as e:
            print(f"[!] Could not update .env: {e}")

def main():
    print("=" * 65)
    print("  SAFERIDE: PUBLIC HTTPS MOBILE TUNNEL")
    print("  Makes WhatsApp Live Tracking URLs work on any mobile device")
    print("=" * 65)
    print("\n[*] Initializing secure public tunnel for port 8000...")

    print("\nAvailable Tunnel Engines:")
    print("  1. Localhost.run (Recommended, Highly Stable SSH)")
    print("  2. Pinggy.io (Fast alternative SSH tunnel)")
    print("  3. Cloudflare (Prone to Error 1033 without account)")
    print("  4. Serveo (Basic fallback)")
    
    # Check if user provided an argument
    if len(sys.argv) > 1:
        choice = sys.argv[1].strip()
    else:
        try:
            choice = input("\nSelect a tunnel engine [1-4] (default 1): ").strip()
        except EOFError:
            choice = '1'

    if choice == '3' and CLOUDFLARED_EXE.exists():
        cmd = [str(CLOUDFLARED_EXE), "tunnel", "--url", "http://127.0.0.1:8000"]
        pattern = r'https://[a-zA-Z0-9_\-\.]+\.trycloudflare\.com'
        print("\n[*] Engine: Cloudflare High-Speed Tunnel")
    elif choice == '4':
        cmd = ["ssh", "-o", "StrictHostKeyChecking=no", "-R", "80:127.0.0.1:8000", "serveo.net"]
        pattern = r'https://[a-zA-Z0-9_\-\.]+\.serveousercontent\.com'
        print("\n[*] Engine: OpenSSH / Serveo fallback")
    elif choice == '2':
        cmd = ["ssh", "-p", "443", "-R0:127.0.0.1:8000", "-o", "StrictHostKeyChecking=no", "a.pinggy.io"]
        pattern = r'https://[a-zA-Z0-9_\-\.]+\.free\.pinggy\.link'
        print("\n[*] Engine: Pinggy.io SSH Tunnel")
    else:
        # Default to localhost.run
        cmd = ["ssh", "-o", "StrictHostKeyChecking=no", "-R", "80:127.0.0.1:8000", "nokey@localhost.run"]
        pattern = r'https://[a-zA-Z0-9_\-\.]+\.lhr\.life'
        print("\n[*] Engine: Localhost.run SSH Tunnel")

    try:
        proc = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1
        )
    except FileNotFoundError:
        print("[ERROR] Tunnel executable not found.")
        sys.exit(1)

    url_detected = False

    try:
        for line in iter(proc.stdout.readline, ''):
            if not line:
                break
            print(line, end='', flush=True)

            match = re.search(pattern, line)
            if match and not url_detected:
                public_url = match.group(0)
                url_detected = True
                update_env_file(public_url)
                print("\n" + "=" * 65)
                print(f"  [SUCCESS] PUBLIC HTTPS TUNNEL ACTIVE:")
                print(f"  {public_url}")
                print(f"  Live Tracking URL Format:")
                print(f"  {public_url}/live-track/<share_token>/")
                print("  Any smartphone on WhatsApp will now load live map updates!")
                print("=" * 65 + "\n")

        proc.wait()
    except KeyboardInterrupt:
        print("\n[*] Stopping tunnel...")
        proc.terminate()
        try:
            proc.wait(timeout=3)
        except subprocess.TimeoutExpired:
            proc.kill()
        print("[*] Tunnel closed.")

if __name__ == '__main__':
    main()
