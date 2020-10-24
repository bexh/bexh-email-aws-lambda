from main.src.core import EmailHandlerOperator
from json import loads
from collections import namedtuple
import os


class VerificationEmailOperator(EmailHandlerOperator):
    def __init__(self, event, context):
        self.VerificationEmailStruct = namedtuple('VerificationEmailStruct', 'email first_name uid token')
        super(VerificationEmailOperator, self).__init__(__name__, event, context)

    def execute(self):
        for record in self.event["Records"]:
            self.process_record(record)

    def process_record(self, record):
        message = self.VerificationEmailStruct(**loads(record["Sns"]["Message"]))
        verification_url = f"{os.environ.get('BASE_URL')}/verification?uid={message.uid}&token={message.token}"
        params = {
            "first_name": message.first_name,
            "verification_url": verification_url
        }
        path = "main/src/app/verification_email/resources/templates/verification_email.html"
        html_template = self.read_html(path)
        html_content = self.template(html_template, params)
        from_email = os.environ.get("BEXH_EMAIL")
        subject = "Please Verify Your Email"
        self.send_email(
            from_email=from_email,
            to_email=message.email,
            subject=subject,
            html_content=html_content
        )
