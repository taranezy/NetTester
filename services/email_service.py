"""
Email Service - Responsible for sending email notifications
Follows Single Responsibility Principle (SRP)
"""
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import Optional


class EmailService:
    """Service to send email notifications."""
    
    def __init__(self, smtp_server: str, smtp_port: int, sender_email: str, 
                 sender_password: str, use_tls: bool = True):
        """
        Initialize the email service.
        
        Args:
            smtp_server: SMTP server address
            smtp_port: SMTP server port
            sender_email: Sender's email address
            sender_password: Sender's email password or app password
            use_tls: Whether to use TLS encryption
        """
        self.smtp_server = smtp_server
        self.smtp_port = smtp_port
        self.sender_email = sender_email
        self.sender_password = sender_password
        self.use_tls = use_tls
    
    def send_notification(self, recipient_email: str, subject: str, message: str) -> bool:
        """
        Send an email notification.
        
        Args:
            recipient_email: Recipient's email address
            subject: Email subject
            message: Email message body
            
        Returns:
            bool: True if email sent successfully, False otherwise
        """
        try:
            # Create message
            msg = MIMEMultipart()
            msg['From'] = self.sender_email
            msg['To'] = recipient_email
            msg['Subject'] = subject
            
            msg.attach(MIMEText(message, 'plain'))
            
            # Connect to SMTP server and send email
            if self.use_tls:
                server = smtplib.SMTP(self.smtp_server, self.smtp_port)
                server.starttls()
            else:
                server = smtplib.SMTP_SSL(self.smtp_server, self.smtp_port)
            
            server.login(self.sender_email, self.sender_password)
            server.send_message(msg)
            server.quit()
            
            return True
            
        except Exception as e:
            print(f"Failed to send email: {e}")
            return False
