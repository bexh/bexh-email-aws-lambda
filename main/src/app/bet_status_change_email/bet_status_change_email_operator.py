from main.src.core import EmailHandlerOperator
from json import loads
import os


class BetStatusChangeEmailOperator(EmailHandlerOperator):
    def __init__(self, event, context):
        self.BET_ACCEPTED_SUBJECT = "BET_ACCEPTED"
        self.BET_DECLINED_SUBJECT = "BET_DECLINED"
        self.BET_EXECUTED_SUBJECT = "BET_EXECUTED"
        self.BET_SUBMITTED_SUBJECT = "BET_SUBMITTED"

        self.email_subject = {
            self.BET_ACCEPTED_SUBJECT: "Your Bet Has Been Accepted!",
            self.BET_DECLINED_SUBJECT: "Your Bet Has Been Declined",
            self.BET_EXECUTED_SUBJECT: "Your Bet Has Been Executed!",
            self.BET_SUBMITTED_SUBJECT: "Your Bet Has Been Submitted!"
        }

        self.template_path = "main/src/app/bet_status_change_email/resources/templates/bet_status_change_email.html"

        self.bet_action = {
            self.BET_ACCEPTED_SUBJECT: "accepted",
            self.BET_DECLINED_SUBJECT: "declined",
            self.BET_EXECUTED_SUBJECT: "executed",
            self.BET_SUBMITTED_SUBJECT: "submitted"
        }

        super(BetStatusChangeEmailOperator, self).__init__(__name__, event, context)

    def execute(self):
        for record in self.event["Records"]:
            self.process_record(record)

    def process_record(self, record):
        sns_subject = record["Sns"]["Subject"]
        message = loads(record["Sns"]["Message"])
        to_email = message["email"],

        subject = self.email_subject[sns_subject]
        bet_action = self.bet_action[sns_subject]

        params = {
            "first_name": message["first_name"],
            "on": message["on"],
            "home": message["home"],
            "away": message["away"],
            "date": message["date"],
            "amount": message["amount"],
            "with": message.get("with"),
            "subject": subject,
            "bet_action": bet_action,
            "odds": message.get("odds")
        }

        html_template = self.read_html(self.template_path)
        html_content = self.template(html_template, params)
        from_email = os.environ.get("BEXH_EMAIL")

        # comment in for testing
        
        # directory = "tmp"
        # path = f"{directory}/test.html"
        # if not os.path.exists(path):
        #     os.makedirs(directory)
        # with open(path, 'w') as f:
        #     f.write(html_content)

        self.send_email(
            from_email=from_email,
            to_email=to_email,
            subject=subject,
            html_content=html_content
        )
