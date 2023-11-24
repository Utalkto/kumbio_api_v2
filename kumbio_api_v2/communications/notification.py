import json
import os

import requests
from mailjet_rest import Client


MAILJET_API_KEY = os.environ.get("MAILJET_API_KEY")
MAILJET_SECRET_KEY = os.environ.get("MAILJET_SECRET_KEY")
MAILJET_EMAIL = os.environ.get("MAILJET_EMAIL")
ULTRAMSG_INSTANCE = os.environ.get("ULTRAMSG_INSTANCE")
ULTRAMSG_TOKEN = os.environ.get("ULTRAMSG_TOKEN")


def send_email(send_to: str, subject: str, html: str, sender: str = "Kumbio Calendar"):
    send_to = send_to
    subject = subject
    html = html

    mailjet: Client = Client(auth=(MAILJET_API_KEY, MAILJET_SECRET_KEY), version="v3.1")

    message = {
        "From": {
            "Email": MAILJET_EMAIL,
            "Name": sender,
        },
        "To": [{"Email": send_to, "Name": "Kumbio Calendar"}],
        "Subject": subject,
        "TextPart": "",
        "HTMLPart": html,
    }

    data = {"Messages": [message]}
    mailjet.send.create(data=data)
    # add error handling


def send_whatsapp(send_to: str, message: str):
    send_to = send_to
    message = message

    url = "https://api.ultramsg.com/" + ULTRAMSG_INSTANCE + "/messages/chat"

    payload = json.dumps(
        {
            "token": ULTRAMSG_TOKEN,
            "to": send_to,
            "body": message,
            "priority": 10,
            "referenceId": "",
            "msgid": "",
            "mentions": "",
        }
    )
    headers = {
        "Content-Type": "application/json",
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    if response.status_code == 200:
        return True
    return False


def replace_message_tags(message: str, data_to_replace: dict) -> str:
    for key, value in data_to_replace.items():
        message = message.replace(f"{{{key}}}", str(value))

    return message
