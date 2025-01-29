import smtplib
import ssl
from email.message import EmailMessage
import mimetypes
import os
from dotenv import load_dotenv


class SMTP_Email:
    def __init__(self, dotenv_path='.env'):
        self.context = ssl.create_default_context()
        self._load_env(dotenv_path)

    def _load_env(self, dotenv_path):
        if load_dotenv(dotenv_path):
            print(f"{dotenv_path} loaded successfully")
        else:
            raise FileNotFoundError(f"Failed to load {dotenv_path}. Ensure the file exists and has the correct format.")

        self.email_sender = os.getenv('EMAIL_SENDER')
        self.email_password = os.getenv('EMAIL_PASSWORD')

        if not self.email_sender or not self.email_password:
            raise ValueError("EMAIL_SENDER or EMAIL_PASSWORD not set in the environment file.")

    def send_email(self, email_receivers, subject, body, pdf_path=None, is_html=False):

        if isinstance(email_receivers, str):
            email_receivers = [email_receivers]

        for email_receiver in email_receivers:
            em = EmailMessage()
            em['From'] = self.email_sender
            em['To'] = email_receiver
            em['Subject'] = subject

            if is_html:
                em.add_alternative(body, subtype='html')
            else:
                em.set_content(body)

            if pdf_path:
                mime_type, _ = mimetypes.guess_type(pdf_path)
                mime_type, mime_subtype = mime_type.split('/')

                with open(pdf_path, 'rb') as pdf_file:
                    em.add_attachment(pdf_file.read(),
                                      maintype=mime_type,
                                      subtype=mime_subtype,
                                      filename=os.path.basename(pdf_path))

            with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=self.context) as smtp:
                smtp.login(self.email_sender, self.email_password)
                smtp.sendmail(self.email_sender, email_receiver, em.as_string())
                print(f"Email sent to: {email_receiver}")
