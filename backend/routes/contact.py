import re
import socket
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
from flask import Blueprint, request, jsonify, current_app
from database import db
from models.message import Message

contact_bp = Blueprint("contact", __name__, url_prefix="/api")

EMAIL_REGEX = r"^[\w\.-]+@[\w\.-]+\.\w+$"

def send_smtp_email(name, email, message_content, is_test=False):
    """
    Sends an email notification via SMTP to the portfolio owner.
    Returns (True, None) on success, or (False, diagnostic_error_message) on failure.
    Logs comprehensive server-side diagnostics without exposing secrets.
    """
    host = current_app.config.get("MAIL_HOST")
    port = current_app.config.get("MAIL_PORT", 587)
    username = current_app.config.get("MAIL_USERNAME")
    password = current_app.config.get("MAIL_PASSWORD")
    use_tls = current_app.config.get("MAIL_USE_TLS", True)
    use_ssl = current_app.config.get("MAIL_USE_SSL", False)
    recipient = current_app.config.get("MAIL_TO", "kathiresantoto@gmail.com")
    sender = current_app.config.get("MAIL_FROM") or f"Portfolio Alert <{recipient}>"

    # 1. Check Missing Environment Variables
    if not host:
        err = "[SMTP ERROR: Missing MAIL_HOST] Host is not configured in backend/.env"
        print(err)
        return False, "MAIL_HOST is not configured."
    if not username:
        err = "[SMTP ERROR: Missing MAIL_USERNAME] Email username is not set in backend/.env"
        print(err)
        return False, "MAIL_USERNAME is not configured."
    if not password:
        err = "[SMTP ERROR: Missing MAIL_PASSWORD] Email password / App Password is empty in backend/.env. Generate a Google App Password at https://myaccount.google.com/apppasswords"
        print(err)
        return False, "MAIL_PASSWORD is not configured."

    try:
        msg = MIMEMultipart("alternative")
        subject = "🧪 Test Email: Portfolio Verification" if is_test else "New Portfolio Contact Message"
        msg["Subject"] = subject
        msg["From"] = sender
        msg["To"] = recipient
        msg["Reply-To"] = email

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
        err = f"[SMTP AUTHENTICATION ERROR] Authentication failed for '{username}'. (Code: {e.smtp_code}). For Gmail, ensure 2-Step Verification is active and you are using a 16-letter App Password from https://myaccount.google.com/apppasswords."
        print(err)
        return False, "SMTP authentication failed. Please verify your MAIL_USERNAME and MAIL_PASSWORD (Google App Password)."

    except (smtplib.SMTPConnectError, socket.timeout, socket.gaierror, TimeoutError, ConnectionRefusedError) as e:
        err = f"[SMTP CONNECTION ERROR] Failed to connect to {host}:{port}. Error: {str(e)}"
        print(err)
        return False, f"Could not connect to SMTP server at {host}:{port}."

    except smtplib.SMTPRecipientsRefused as e:
        err = f"[SMTP RECIPIENT REJECTED] The mail provider rejected recipient {recipient}. Error: {str(e)}"
        print(err)
        return False, f"Recipient address rejected by mail server."

    except smtplib.SMTPSenderRefused as e:
        err = f"[SMTP SENDER REJECTED] The mail provider rejected sender {sender}. Error: {str(e)}"
        print(err)
        return False, f"Sender address rejected by mail server."

    except smtplib.SMTPException as e:
        err = f"[SMTP PROTOCOL ERROR] SMTP protocol exception: {str(e)}"
        print(err)
        return False, f"SMTP protocol error occurred."

    except Exception as e:
        err = f"[SMTP UNEXPECTED ERROR] {str(e)}"
        print(err)
        return False, f"Unexpected error while sending email."

@contact_bp.route("/contact", methods=["POST"])
def submit_contact_form():
    """
    Handle visitor contact form submissions:
    1. Validates submitted name, email, and message.
    2. Saves message into MySQL / SQLite messages table.
    3. Attempts actual SMTP email sending to kathiresantoto@gmail.com.
    4. Returns 200 success ONLY if email succeeds; otherwise returns 500 error.
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

    # 2. Dispatch real email via SMTP
    email_success, email_error = send_smtp_email(name, email, message)

    # 3. Return exact responses
    if not email_success:
        return jsonify({
            "success": False,
            "message": "Unable to send your message right now."
        }), 500

    return jsonify({
        "success": True,
        "message": "Your message has been sent successfully."
    }), 200

@contact_bp.route("/test-email", methods=["GET", "POST"])
def test_email_endpoint():
    """
    Dedicated diagnostic endpoint to test real email dispatch to kathiresantoto@gmail.com.
    """
    recipient = current_app.config.get("MAIL_TO", "kathiresantoto@gmail.com")
    username = current_app.config.get("MAIL_USERNAME")
    has_password = bool(current_app.config.get("MAIL_PASSWORD"))

    if not has_password:
        return jsonify({
            "success": False,
            "message": "MAIL_PASSWORD is not configured in backend/.env. Please set your 16-character Google App Password.",
            "diagnostics": {
                "mail_host": current_app.config.get("MAIL_HOST"),
                "mail_port": current_app.config.get("MAIL_PORT"),
                "mail_username": username,
                "recipient": recipient,
                "password_configured": False
            }
        }), 400

    email_success, email_error = send_smtp_email(
        name="SMTP Verification Tool",
        email="test-mailer@kathiresan-portfolio.local",
        message_content="This is an automated test email confirming real email delivery to kathiresantoto@gmail.com is fully functional.",
        is_test=True
    )

    if not email_success:
        return jsonify({
            "success": False,
            "message": f"Test email failed: {email_error}",
            "diagnostics": {
                "mail_host": current_app.config.get("MAIL_HOST"),
                "mail_port": current_app.config.get("MAIL_PORT"),
                "mail_username": username,
                "recipient": recipient,
                "password_configured": True
            }
        }), 500

    return jsonify({
        "success": True,
        "message": f"Test email successfully sent to {recipient}!",
        "diagnostics": {
            "mail_host": current_app.config.get("MAIL_HOST"),
            "mail_port": current_app.config.get("MAIL_PORT"),
            "mail_username": username,
            "recipient": recipient,
            "password_configured": True
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
