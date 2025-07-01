import base64
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

SCOPES = ['https://www.googleapis.com/auth/gmail.send']



def send_alert_email(to, subject, employee_name):# done
    try:
        with open('alert_email.html', 'r') as f:
            message_text = f.read()


        message_text = message_text.replace('{{ employee_name }}', employee_name)

        creds = Credentials.from_authorized_user_file('jungle_clock_out.json', SCOPES)
        service = build('gmail', 'v1', credentials=creds)

        message = MIMEMultipart()
        message['from'] = 'JungleClock <noreplay@jungleclock.com>'
        message['to'] = to
        message['subject'] = subject
        message.attach(MIMEText(message_text, 'html'))

        raw_message = base64.urlsafe_b64encode(message.as_bytes()).decode()
        body = {'raw': raw_message}

        message = service.users().messages().send(userId='me', body=body).execute()
        #print(f"Message sent! Message Id: {message['id']}")
        return True

    except HttpError as e:
        #print(f'An error occurred: {e}')
        #return str(e)
        return False
