from __future__ import print_function

import base64
import datetime
import os
from email.message import EmailMessage

import google.auth
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError


def send_email(to: str = 'david.h.pitt@gmail.com', subject:str = 'Your morning briefing', body: str = './message.txt'):
    """Create and send an email message.
       Print the returned message and id.
       Returns: Message object, including draft id and message meta data.

      Load pre-authorized user credentials from the environment.
      TODO(developer) - See https://developers.google.com/identity
      for guides on implementing OAuth2 for the application.
    """
    SCOPES = ['https://www.googleapis.com/auth/gmail.compose']

    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    try:
        service = build('gmail', 'v1', credentials=creds)
        message = EmailMessage()

        message['To'] = to
        message['From'] = 'autobriefme@gmail.com'
        message['Subject'] = subject

        with open(body, "r") as f:
            content = ''.join(f.readlines())
        message.set_content(content)


        # encoded message
        encoded_message = base64.urlsafe_b64encode(message.as_bytes()) \
            .decode()

        create_message = {
            'raw': encoded_message
        }
        # pylint: disable=E1101
        send_message = (service.users().messages().send
                        (userId="me", body=create_message).execute())
        print(F'Message sent with ID: {send_message["id"]}')
    except HttpError as error:
        print(F'An error occurred: {error}')
        send_message = None
    return send_message


if __name__ == '__main__':
    todays_date = datetime.date.today()
    subject_str = f'{todays_date.month}/{todays_date.day}: your morning briefing'
    send_email(to='david.h.pitt@gmail.com', body='./message.txt', subject=subject_str)