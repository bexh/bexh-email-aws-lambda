import os

from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

from main.src.logger import Logger


class Mailer:
    def __init__(self, logger: Logger, api_key: str):
        self.sg = SendGridAPIClient(api_key)
        self.logger = logger

    def send_message(self, from_email: str, to_email: str, subject: str, html_content: str):
        self.logger.info(f"Sending email from {from_email} to {to_email} with subject {subject}")
        message = Mail(
            from_email=from_email,
            to_emails=to_email,
            subject=subject,
            html_content=html_content)
        try:
            response = self.sg.send(message)
            self.logger.info(f"mailer status_code: {response.status_code}")
            headers = str(response.headers).replace('\n', ' ')
            self.logger.info(f"mailer response: {response.body}")
            self.logger.info(f"mailer headers: {headers}")
        except Exception as e:
            self.logger.error(f"mailer error message: {e.message}")
            raise e


class MailerFactory:
    def __init__(self):
        self.api_key = os.environ.get("TWILIO_API_KEY")

    def get_mailer(self, logger: Logger) -> Mailer:
        return Mailer(logger=logger, api_key=self.api_key)
