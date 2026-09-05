import re
import json
import socket
import smtplib
import urllib.request
import urllib.error
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
from flask import Blueprint, request, jsonify, current_app
from database import db
from models.message import Message

contact_bp = Blueprint("contact", __name__, url_prefix="/api")

EMAIL_REGEX = r"^[\w\.-]+@[\w\.-]+\.\w+$"

def _build_email_templates(name, email, message_content, is_test=False):
    """Generate both HTML and plain-text email templates."""
    subject = "🧪 Test Email: Portfolio Verification" if is_test else f"Portfolio Message from {name}"
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    plain_text = f"""Name: {name}
Email: {email}
Date: {timestamp}

Message:
{message_content}
"""

    html_content = f"""
    <html>
      <body style="font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; background-color: #090d16; color: #f8fafc; padding: 24px; margin: 0;">
        <div style="max-width: 600px; margin: 0 auto; background: #0f172a; border-radius: 12px; border: 1px solid rgba(255,255,255,0.1); overflow: hidden;">
          <div style="background: linear-gradient(135deg, #3b82f6, #06b6d4); padding: 20px 24px;">
            <h2 style="margin: 0; color: #ffffff; font-size: 20px;">{subject}</h2>
            <p style="margin: 4px 0 0; color: #e2e8f0; font-size: 14px;">Kathiresan Portfolio Inbound Notification</p>
          </div>
          <div style="padding: 24px;">
            <p style="margin: 0 0 16px; font-size: 14px; color: #94a3b8;">
              You have received a new message from your portfolio contact form:
            </p>
            <div style="background: #1e293b; border-radius: 8px; padding: 16px; margin-bottom: 20px;">
              <p style="margin: 0 0 8px; color: #cbd5e1; font-size: 14px;"><strong>Name:</strong> {name}</p>
              <p style="margin: 0 0 8px; color: #cbd5e1; font-size: 14px;"><strong>Email:</strong> <a href="mailto:{email}" style="color: #38bdf8; text-decoration: none;">{email}</a></p>
              <p style="margin: 0; color: #94a3b8; font-size: 13px;"><strong>Date:</strong> {timestamp}</p>
            </div>
            <div style="background: #1e293b; border-radius: 8px; padding: 16px; border-left: 4px solid #3b82f6;">
              <strong style="color: #94a3b8; font-size: 12px; text-transform: uppercase; letter-spacing: 0.5px;">Message:</strong>
              <p style="margin: 8px 0 0; color: #f8fafc; font-size: 15px; line-height: 1.6; white-space: pre-wrap;">{message_content}</p>
            </div>
            <div style="margin-top: 24px; text-align: center;">
              <a href="mailto:{email}?subject=Re:%20Portfolio%20Inquiry" style="display: inline-block; background: #2563eb; color: #ffffff; text-decoration: none; padding: 10px 22px; border-radius: 6px; font-weight: 600; font-size: 14px;">
                Reply to {name}
              </a>
            </div>
          </div>
        </div>
      </body>
    </html>
    """
    return subject, plain_text, html_content


def _make_http_email_request(url, headers, payload, provider="Resend"):
    """Execute outbound HTTPS email delivery via REST API."""
    try:
        data = json.dumps(payload).encode("utf-8")
        req = urllib.request.Request(url, data=data, headers=headers, method="POST")
        with urllib.request.urlopen(req, timeout=12) as response:
            status_code = response.getcode()
            if status_code in (200, 201, 202):
                print(f"[HTTP EMAIL SUCCESS] Email delivered via {provider} API (HTTP {status_code}).")
                return True, None
            else:
                return False, f"{provider} API returned unexpected status code: {status_code}"
    except urllib.error.HTTPError as e:
        error_body = ""
        try:
            error_body = e.read().decode("utf-8", errors="ignore")
        except Exception:
            pass
        print(f"[HTTP EMAIL ERROR] {provider} API returned HTTP {e.code}: {error_body}")
        if e.code in (401, 403):
            return False, f"Invalid {provider} API key. Please check your {provider.upper()}_API_KEY."
        elif e.code == 422:
            return False, f"Invalid recipient or sender format in {provider} configuration."
        return False, f"Email delivery service ({provider}) returned error code {e.code}."
    except Exception as e:
        print(f"[HTTP EMAIL ERROR] Connection to {provider} API failed: {str(e)}")
        return False, f"Could not connect to {provider} email delivery service."


def send_http_api_email(name, email, message_content, is_test=False):
    """
    Sends an email notification via serverless-friendly HTTP REST APIs.
    Supports Resend (recommended), SendGrid, and Brevo over HTTPS Port 443.
    """
    resend_key = current_app.config.get("RESEND_API_KEY")
    sendgrid_key = current_app.config.get("SENDGRID_API_KEY")
    brevo_key = current_app.config.get("BREVO_API_KEY")
    recipient = current_app.config.get("MAIL_TO", "kathiresantoto@gmail.com")

    subject, plain_text, html_content = _build_email_templates(name, email, message_content, is_test=is_test)

    # Provider 1: Resend (Default / Recommended)
    if resend_key:
        from_address = current_app.config.get("RESEND_FROM") or "Kathiresan Portfolio <onboarding@resend.dev>"
        payload = {
            "from": from_address,
            "to": [recipient],
            "reply_to": email,
            "subject": subject,
            "html": html_content,
            "text": plain_text
        }
        url = "https://api.resend.com/emails"
        headers = {
            "Authorization": f"Bearer {resend_key}",
            "Content-Type": "application/json",
            "User-Agent": "Kathiresan-Portfolio/1.0"
        }
        return _make_http_email_request(url, headers, payload, provider="Resend")

    # Provider 2: SendGrid
    elif sendgrid_key:
        from_email = current_app.config.get("MAIL_FROM") or "kathiresantoto@gmail.com"
        from_match = re.search(r"<([^>]+)>", from_email)
        clean_from = from_match.group(1) if from_match else from_email

        payload = {
            "personalizations": [{"to": [{"email": recipient}]}],
            "from": {"email": clean_from, "name": "Kathiresan Portfolio"},
            "reply_to": {"email": email, "name": name},
            "subject": subject,
            "content": [{"type": "text/html", "value": html_content}]
        }
        url = "https://api.sendgrid.com/v3/mail/send"
        headers = {
            "Authorization": f"Bearer {sendgrid_key}",
            "Content-Type": "application/json",
            "User-Agent": "Kathiresan-Portfolio/1.0"
        }
        return _make_http_email_request(url, headers, payload, provider="SendGrid")

    # Provider 3: Brevo (Sendinblue)
    elif brevo_key:
        payload = {
            "sender": {"name": "Kathiresan Portfolio", "email": recipient},
            "to": [{"email": recipient}],
            "replyTo": {"email": email, "name": name},
            "subject": subject,
            "htmlContent": html_content
        }
        url = "https://api.brevo.com/v3/smtp/email"
        headers = {
            "api-key": brevo_key,
            "Content-Type": "application/json",
            "User-Agent": "Kathiresan-Portfolio/1.0"
        }
        return _make_http_email_request(url, headers, payload, provider="Brevo")

    return False, "No HTTP email API key configured. Please set RESEND_API_KEY in Vercel environment variables."


def send_smtp_email(name, email, message_content, is_test=False):
    """
    Sends an email notification via SMTP (retained for local development).
    """
    host = current_app.config.get("MAIL_HOST") or "smtp.gmail.com"
    port = int(current_app.config.get("MAIL_PORT") or 587)
    username = (current_app.config.get("MAIL_USERNAME") or "").strip()
    password = (current_app.config.get("MAIL_PASSWORD") or "").strip()
    use_ssl = current_app.config.get("MAIL_USE_SSL", False) or port == 465
    use_tls = current_app.config.get("MAIL_USE_TLS", True) and not use_ssl
    recipient = current_app.config.get("MAIL_TO", "kathiresantoto@gmail.com")
    sender = current_app.config.get("MAIL_FROM") or f"Portfolio Alert <{recipient}>"

    if not username:
        return False, "MAIL_USERNAME is not configured."
    if not password:
        return False, "MAIL_PASSWORD is not configured."

    try:
        subject, plain_text, html_content = _build_email_templates(name, email, message_content, is_test=is_test)

        msg = MIMEMultipart("alternative")
        msg["Subject"] = subject
        msg["From"] = sender
        msg["To"] = recipient
        msg["Reply-To"] = email

        msg.attach(MIMEText(plain_text, "plain"))
        msg.attach(MIMEText(html_content, "html"))

        print(f"[SMTP] Connecting to mail server {host}:{port} (SSL={use_ssl}, TLS={use_tls})...")

        if use_ssl:
            server = smtplib.SMTP_SSL(host, port, timeout=12)
        else:
            server = smtplib.SMTP(host, port, timeout=12)
            if use_tls:
                server.starttls()

        print(f"[SMTP] Authenticating with user: {username}...")
        server.login(username, password)

        print(f"[SMTP] Sending message to {recipient}...")
        server.send_message(msg)
        server.quit()

        print(f"[SMTP SUCCESS] Email successfully dispatched to {recipient}!")
        return True, None

    except smtplib.SMTPAuthenticationError as e:
        err = f"[SMTP AUTHENTICATION ERROR] Authentication failed for '{username}'. (Code: {e.smtp_code})."
        print(err)
        return False, "SMTP authentication failed. Please verify your MAIL_USERNAME and MAIL_PASSWORD."

    except (smtplib.SMTPConnectError, socket.timeout, socket.gaierror, TimeoutError, ConnectionRefusedError, OSError) as e:
        err = f"[SMTP CONNECTION ERROR] Failed to connect to {host}:{port}. Error: {str(e)}"
        print(err)
        return False, f"Could not connect to SMTP server at {host}:{port} ({str(e)})."

    except Exception as e:
        err = f"[SMTP UNEXPECTED ERROR] {str(e)}"
        print(err)
        return False, f"SMTP error while sending email: {str(e)}"


def dispatch_email(name, email, message_content, is_test=False):
    """
    Unified email dispatcher:
    1. Attempts serverless-native HTTP Email API (Resend, SendGrid, Brevo) first.
    2. Falls back to SMTP for local development if MAIL_PASSWORD is configured.
    """
    has_http_api = bool(
        current_app.config.get("RESEND_API_KEY") or
        current_app.config.get("SENDGRID_API_KEY") or
        current_app.config.get("BREVO_API_KEY")
    )

    if has_http_api:
        return send_http_api_email(name, email, message_content, is_test=is_test)

    # Fallback to local SMTP if MAIL_PASSWORD is provided
    if current_app.config.get("MAIL_PASSWORD"):
        return send_smtp_email(name, email, message_content, is_test=is_test)

    return False, "Email service is not configured. Please set RESEND_API_KEY in Vercel environment variables."


@contact_bp.route("/contact", methods=["POST"])
def submit_contact_form():
    """
    Handle visitor contact form submissions:
    1. Validates submitted name, email, and message.
    2. Saves message into MySQL / SQLite messages table.
    3. Attempts email delivery via HTTP API (production) or SMTP (local).
    4. Returns 200 success on delivery, or 500 with diagnostic message.
    """
    data = request.get_json() or {}

    # Anti-spam Honeypot Check
    if data.get("_gotcha") or data.get("website_url"):
        return jsonify({"success": False, "message": "Spam detected."}), 400

    name = data.get("name", "").strip()
    email = data.get("email", "").strip()
    message = data.get("message", "").strip()

    # Input validations
    if not name:
        return jsonify({"success": False, "message": "Please provide your name."}), 400
    if not email or not re.match(EMAIL_REGEX, email):
        return jsonify({"success": False, "message": "Please provide a valid email address."}), 400
    if not message or len(message) < 5:
        return jsonify({"success": False, "message": "Message must be at least 5 characters long."}), 400

    # 1. Save entry to database
    try:
        new_msg = Message(
            name=name,
            email=email,
            message=message
        )
        db.session.add(new_msg)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        print(f"[DATABASE ERROR] Failed to save message: {e}")
        return jsonify({"success": False, "message": "Message could not be saved to database."}), 500

    # 2. Dispatch real email via unified dispatcher
    email_success, email_error = dispatch_email(name, email, message)

    # 3. Return exact responses
    if not email_success:
        return jsonify({
            "success": False,
            "message": email_error or "Unable to send your message right now."
        }), 500

    return jsonify({
        "success": True,
        "message": "Your message has been sent successfully."
    }), 200


@contact_bp.route("/test-email", methods=["GET", "POST"])
def test_email_endpoint():
    """
    Diagnostic endpoint to test email dispatch to kathiresantoto@gmail.com.
    """
    recipient = current_app.config.get("MAIL_TO", "kathiresantoto@gmail.com")
    has_resend = bool(current_app.config.get("RESEND_API_KEY"))
    has_sendgrid = bool(current_app.config.get("SENDGRID_API_KEY"))
    has_brevo = bool(current_app.config.get("BREVO_API_KEY"))
    has_smtp = bool(current_app.config.get("MAIL_PASSWORD"))

    if not (has_resend or has_sendgrid or has_brevo or has_smtp):
        return jsonify({
            "success": False,
            "message": "Email delivery is not configured. Please add RESEND_API_KEY in Vercel environment variables.",
            "diagnostics": {
                "resend_configured": False,
                "sendgrid_configured": False,
                "brevo_configured": False,
                "smtp_configured": False,
                "recipient": recipient
            }
        }), 400

    email_success, email_error = dispatch_email(
        name="Portfolio Diagnostic Suite",
        email="test-mailer@kathiresan-portfolio.local",
        message_content="This is an automated test email confirming real email delivery to kathiresantoto@gmail.com is fully functional.",
        is_test=True
    )

    if not email_success:
        return jsonify({
            "success": False,
            "message": f"Test email failed: {email_error}",
            "diagnostics": {
                "resend_configured": has_resend,
                "sendgrid_configured": has_sendgrid,
                "brevo_configured": has_brevo,
                "smtp_configured": has_smtp,
                "recipient": recipient
            }
        }), 500

    return jsonify({
        "success": True,
        "message": f"Test email successfully dispatched to {recipient}!",
        "diagnostics": {
            "resend_configured": has_resend,
            "sendgrid_configured": has_sendgrid,
            "brevo_configured": has_brevo,
            "recipient": recipient
        }
    }), 200


@contact_bp.route("/messages", methods=["GET"])
def get_messages():
    """Retrieve all received contact messages from database."""
    try:
        messages = Message.query.order_by(Message.created_at.desc()).all()
        return jsonify({
            "success": True,
            "count": len(messages),
            "data": [m.to_dict() for m in messages]
        }), 200
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500
