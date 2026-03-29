import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from dotenv import dotenv_values
import os

config = dotenv_values(".env")

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class EmailNotifications:
    def send_email_notification(emailBody, html_template):
        EMAIL_HOST = config['EMAIL_HOST']
        EMAIL_PASSWORD = config['EMAIL_PASSWORD']
        EMAIL_USER = config['EMAIL_USER']
        EMAIL_PORT = config['EMAIL_PORT']
        DEFAULT_FROM_EMAIL = config['DEFAULT_FROM_EMAIL']
        
        reset_url = emailBody.get('url', '')
        
        template_path = os.path.join(BASE_DIR, 'rent_ms_backend_html', 'templates', html_template)
        
        with open(template_path, 'r') as f:
            html_content = f.read()
        
        html_content = html_content.replace('{{ data.url }}', reset_url)
        
        if emailBody.get('user'):
            user = emailBody['user']
            first_name = getattr(user, 'first_name', '') or ''
            html_content = html_content.replace('{{ data.user.first_name }}', first_name)
        
        text_content = f"Password Reset Request\n\nClick the link below to reset your password:\n{reset_url}\n\nIf you didn't request this, please ignore this email."
        
        msg = MIMEMultipart()
        msg['From'] = DEFAULT_FROM_EMAIL
        msg['To'] = emailBody['receiver_details']
        msg['Subject'] = emailBody['subject']

        msg.attach(MIMEText(text_content, 'plain'))
        msg.attach(MIMEText(html_content, 'html'))
        
        server = smtplib.SMTP(EMAIL_HOST, EMAIL_PORT)
        server.starttls()

        server.login(EMAIL_USER, EMAIL_PASSWORD)

        server.sendmail(DEFAULT_FROM_EMAIL, emailBody['receiver_details'], msg.as_string())

        server.quit()

        return True