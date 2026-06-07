"""
Email service for sending notifications and campaigns
"""
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import logging

logger = logging.getLogger(__name__)

class EmailService:
    def __init__(self):
        self.smtp_server = os.getenv("SMTP_SERVER", "smtp.gmail.com")
        self.smtp_port = int(os.getenv("SMTP_PORT", 587))
        self.sender_email = os.getenv("SENDER_EMAIL")
        self.sender_password = os.getenv("SENDER_PASSWORD")
    
    def send_email(self, to_email: str, subject: str, body: str, html: bool = False) -> bool:
        """Send email"""
        try:
            msg = MIMEMultipart('alternative')
            msg['Subject'] = subject
            msg['From'] = self.sender_email
            msg['To'] = to_email
            
            if html:
                msg.attach(MIMEText(body, 'html'))
            else:
                msg.attach(MIMEText(body, 'plain'))
            
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(self.sender_email, self.sender_password)
                server.send_message(msg)
            
            logger.info(f"Email sent to {to_email}")
            return True
        except Exception as e:
            logger.error(f"Failed to send email: {e}")
            return False
    
    def send_lead_notification(self, lead_name: str, lead_email: str, lead_platform: str) -> bool:
        """Send notification to admin about new lead"""
        admin_email = os.getenv("ADMIN_EMAIL")
        subject = f"🎉 New Lead: {lead_name}"
        body = f"""
        <h2>New Lead Captured!</h2>
        <p><strong>Name:</strong> {lead_name}</p>
        <p><strong>Email:</strong> {lead_email}</p>
        <p><strong>Platform:</strong> {lead_platform}</p>
        <p><a href="http://localhost:8000/admin">View in Admin Panel</a></p>
        """
        return self.send_email(admin_email, subject, body, html=True)
    
    def send_welcome_email(self, lead_email: str, lead_name: str) -> bool:
        """Send welcome email to captured lead"""
        subject = "Welcome to AutoStream!"
        body = f"""
        <h2>Hi {lead_name}! 👋</h2>
        <p>Thank you for your interest in AutoStream!</p>
        <p>Our team will contact you shortly with personalized recommendations.</p>
        <p>In the meantime, check out our resources:</p>
        <ul>
            <li><a href="#">Getting Started Guide</a></li>
            <li><a href="#">Feature Overview</a></li>
            <li><a href="#">Pricing Details</a></li>
        </ul>
        <p>Best regards,<br>AutoStream Team</p>
        """
        return self.send_email(lead_email, subject, body, html=True)

# Initialize email service
email_service = EmailService()
