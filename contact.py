from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from mailjet_rest import Client
from dotenv import load_dotenv
import os
import requests

load_dotenv()
API_KEY = os.getenv('MAILJET_API_KEY')
SECRET_API_KEY = os.getenv('MAILJET_SECRET_API_KEY')
SENDER_URL = "https://api.mailjet.com/v3/REST/sender"


def send_mail(username, message, from_email, user_email, to_email):
    msg = MIMEMultipart()
    msg['Subject'] = f"{username} - Contact Response"
    msg['From'] = user_email
    msg['To'] = to_email

    # attach the email content
    msg.attach(MIMEText(message + f"\n\nMessage sent from {user_email}", 'plain'))

    mailjet = Client(auth=(API_KEY, SECRET_API_KEY), version='v3.1')

    data = {
        'Messages': [
            {
                "From": {
                    "Email": from_email,
                    "Name": "Michał Ślęzak"
                },
                "To": [
                    {
                        "Email": to_email,
                        "Name": "Michał Ślęzak"
                    }
                ],
                "Subject": f"{username} - Response",
                "TextPart": msg.as_string(),
                # "HTMLPart": msg.as_string()
            }
        ]
    }

    result = mailjet.send.create(data=data)
    print(result.status_code)
    print(result.json())
