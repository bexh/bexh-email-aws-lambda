import json

from main.src.app.bet_status_change_email.bet_status_change_email_operator import BetStatusChangeEmailOperator


def handler(event, context):
    BetStatusChangeEmailOperator(event, context)


if __name__ == "__main__":
    with open("main/test/resources/bet_submitted_exchange_event.json") as f:
        test_event = json.load(f)
    handler(test_event, None)
