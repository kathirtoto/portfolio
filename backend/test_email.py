#!/usr/bin/env python3
"""
Diagnostic Email Tester for Kathiresan's Developer Portfolio
Usage: python backend/test_email.py
"""

import os
import sys
import socket
import smtplib
from pathlib import Path
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime

# Configure utf-8 stdout for Windows consoles
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

# Load .env file from backend directory
BASE_DIR = Path(__file__).resolve().parent
from dotenv import load_dotenv
load_dotenv(BASE_DIR / ".env")

def test_smtp_configuration():
    print("=" * 60)
    print("[EMAIL TEST] KATHIRESAN PORTFOLIO - SMTP DIAGNOSTIC SUITE")
    print("=" * 60)

    host = os.getenv("MAIL_HOST") or os.getenv("EMAIL_HOST", "smtp.gmail.com")
    port = int(os.getenv("MAIL_PORT") or os.getenv("EMAIL_PORT", 587))
    use_tls = (os.getenv("MAIL_USE_TLS") or os.getenv("EMAIL_USE_TLS", "True")).lower() in ("true", "1", "t")
    use_ssl = (os.getenv("MAIL_USE_SSL") or os.getenv("EMAIL_USE_SSL", "False")).lower() in ("true", "1", "t")
    username = (os.getenv("MAIL_USERNAME") or os.getenv("EMAIL_USERNAME", "kathiresantoto@gmail.com")).strip()
    password = (os.getenv("MAIL_PASSWORD") or os.getenv("EMAIL_PASSWORD", "")).strip()
    recipient = (os.getenv("MAIL_TO") or os.getenv("EMAIL_TO", "kathiresantoto@gmail.com")).strip()
    sender = (os.getenv("MAIL_FROM") or os.getenv("EMAIL_FROM", f"Portfolio Tester <{recipient}>")).strip()

    print(f"[*] SMTP Host       : {host}")
    print(f"[*] SMTP Port       : {port}")
    print(f"[*] Protocol        : {'SSL' if use_ssl else ('TLS (STARTTLS)' if use_tls else 'Plain')}")
    print(f"[*] SMTP Username   : {username}")
    print(f"[*] Recipient Email : {recipient}")
    print(f"[*] Password Status : {'[CONFIGURED]' if password else '[NOT SET - MISSING IN .env]'}")
    print("-" * 60)

    if not password:
        print("\n[!] STATUS: MAIL_PASSWORD is empty in backend/.env.")
        print("\n[HOW TO CONFIGURE REAL EMAIL DELIVERY]:")
        print("1. Visit: https://myaccount.google.com/apppasswords")
        print("2. Ensure 2-Step Verification is active on your Google account.")
        print("3. Generate a 16-character App Password (e.g., 'abcd efgh ijkl mnop').")
        print("4. Paste it into backend/.env under MAIL_PASSWORD=...")
        print("5. Re-run: python backend/test_email.py")
        print("=" * 60)
        return False

    # 1. Socket resolution test
    print("\n[Step 1/4] Resolving host DNS & testing TCP connection...")
    try:
        sock = socket.create_connection((host, port), timeout=8)
        sock.close()
        print("  [OK] Host connection established.")
    except Exception as e:
        print(f"  [ERROR] Connection failed to {host}:{port}: {e}")
        return False

    # 2. SMTP Handshake
    print("[Step 2/4] Initializing SMTP handshake & encryption...")
    try:
        if use_ssl:
            server = smtplib.SMTP_SSL(host, port, timeout=10)
        else:
            server = smtplib.SMTP(host, port, timeout=10)
            if use_tls:
                server.starttls()
        print("  [OK] SMTP handshake and TLS encryption established.")
    except Exception as e:
        print(f"  [ERROR] SMTP Handshake error: {e}")
        return False

    # 3. Authentication
    print(f"[Step 3/4] Authenticating with user '{username}'...")
    try:
        server.login(username, password)
        print("  [OK] SMTP Authentication SUCCESSFUL!")
    except smtplib.SMTPAuthenticationError as e:
        print(f"  [ERROR] Authentication failed (code {e.smtp_code}):")
        print("     Google rejected the credentials.")
        print("     Ensure you generated a 16-character App Password (not your personal Google account password).")
        server.quit()
        return False
    except Exception as e:
        print(f"  [ERROR] Login error: {e}")
        server.quit()
        return False

    # 4. Message Dispatch
    print(f"[Step 4/4] Sending test message to {recipient}...")
    try:
        msg = MIMEMultipart("alternative")
        msg["Subject"] = "Live Verification: Kathiresan Portfolio Email Delivery"
        msg["From"] = sender
        msg["To"] = recipient

        now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        body = f"""Hello Kathiresan,

This email confirms that your portfolio contact form is connected and successfully delivering real messages to {recipient}.

Timestamp: {now_str}
Status: VERIFIED & OPERATIONAL
"""
        msg.attach(MIMEText(body, "plain"))
        server.send_message(msg)
        server.quit()
        print(f"  [OK] Test email successfully dispatched to {recipient}!")
        print("\n" + "=" * 60)
        print("[SUCCESS] Real email delivered! Check your inbox at kathiresantoto@gmail.com.")
        print("=" * 60)
        return True
    except Exception as e:
        print(f"  [ERROR] Failed to send test message: {e}")
        return False

if __name__ == "__main__":
    test_smtp_configuration()
