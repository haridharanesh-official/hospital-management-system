import smtplib
import ssl
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import os
from config import EMAIL_HOST, EMAIL_PORT, EMAIL_USER, EMAIL_PASSWORD  # Import email config

def send_email(to_email, subject, body, attachment_path=None):
    """
    Sends an email with optional attachment.
    
    :param to_email: Recipient email address.
    :param subject: Email subject.
    :param body: Email body (HTML supported).
    :param attachment_path: Path to file to attach (optional).
    """
    try:
        # Create email message
        msg = MIMEMultipart()
        msg['From'] = EMAIL_USER
        msg['To'] = to_email
        msg['Subject'] = subject

        # Attach email body
        msg.attach(MIMEText(body, 'html'))

        # Attach file if provided
        if attachment_path and os.path.exists(attachment_path):
            with open(attachment_path, "rb") as attachment:
                part = MIMEBase("application", "octet-stream")
                part.set_payload(attachment.read())
                encoders.encode_base64(part)
                part.add_header(
                    "Content-Disposition",
                    f"attachment; filename={os.path.basename(attachment_path)}",
                )
                msg.attach(part)

        # Connect to SMTP server
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL(EMAIL_HOST, EMAIL_PORT, context=context) as server:
            server.login(EMAIL_USER, EMAIL_PASSWORD)
            server.sendmail(EMAIL_USER, to_email, msg.as_string())

        print(f"✅ Email sent successfully to {to_email}")

    except Exception as e:
        print(f"❌ Failed to send email: {str(e)}")

# Example usage:
if __name__ == "__main__":
    test_email = "doctor@example.com"
    subject = "🚨 Emergency Alert: Patient Heart Rate Critical!"
    body = """
    <h2>Emergency Alert</h2>
    <p>Patient <b>John Doe</b> has an abnormal heart rate. Immediate attention required!</p>
    """
    send_email(test_email, subject, body)
