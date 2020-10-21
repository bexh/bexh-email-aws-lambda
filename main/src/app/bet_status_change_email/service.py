import json


def handler(event, context):
    print("Starting...")

    return result


if __name__ == "__main__":
    with open("main/test/resources/event.json") as f:
        test_event = json.load(f)
    handler(test_event, None)
