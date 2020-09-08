import base64
from email.mime.text import MIMEText
from typing import Any

from googleAuth import Authenticate
from googleapiclient.errors import HttpError


def create_message(to, jsonData):
    message_text = f"ID: {jsonData['uuid']} \nKey: {jsonData['key']}"
    message = MIMEText(message_text)
    message['to'] = to
    message['from'] = "me"
    message['subject'] = "From Steganography"
    raw = base64.urlsafe_b64encode(message.as_bytes())
    raw = raw.decode()
    return {'raw': raw}


def sendEmail(m: Any):
    service = Authenticate()
    try:
        messsage = (service.users().messages().send(userId="me", body=m).execute())
        # print(f'Message id: {messsage[id]}')
        return messsage
    except HttpError as error:
        print(f'Error occured: {error}')


if __name__ == "__main__":
    jsonData = {'uuid': 12345, 'key': 12312333, 'data': 'sadkjasdkjh'}
    message = create_message('loukikstudent@gmail.com', jsonData)
    print(message)
    m = sendEmail(message)
    print(m)
    print(type(m))
