from main.src.core import EmailHandlerOperator


class VerificationEmailOperator(EmailHandlerOperator):
    def __init__(self, event, context):
        super(VerificationEmailOperator, self).__init__(__name__, event, context)

    def execute(self):
        path = "main/src/app/verification_email/resources/templates/verification_email.html"
        params = {
            "first_name": "Seth",
            "verification_url": "https://google.com"
        }
        html_template = self.read_html(path)
        html_content = self.template(html_template, params)
        from_email = "bexh.dev@gmail.com"
        to_email = "sethsaps@gmail.com"
        subject = "test"
        self.send_email(
            from_email=from_email,
            to_email=to_email,
            subject=subject,
            html_content=html_content
        )
