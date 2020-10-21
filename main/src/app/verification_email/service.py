import json

from main.src.app.verification_email.verification_email_operator import VerificationEmailOperator


def handler(event, context):
    VerificationEmailOperator(event, context)


if __name__ == "__main__":
    with open("main/test/resources/verification_event.json") as f:
        test_event = json.load(f)
    handler(test_event, None)
