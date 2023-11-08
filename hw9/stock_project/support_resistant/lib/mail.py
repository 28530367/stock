import smtplib 
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import datetime
import pathlib
import json
from django.conf import settings

media_path = settings.MEDIA_DIRS_PATH

class MailHandler:
    _host_email_address: str
    _host_passwd: str
    _subject: str

    def __init__(self):
        gmail_acct = f"{media_path}/gmail.json"
        with open(gmail_acct, 'r') as f:
            acct_info = json.load(f)
        self._host_email_address = acct_info["username"]
        self._host_passwd = acct_info["password"]
        self._smtp = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        self._smtp.ehlo()
        self._smtp.login(self._host_email_address, self._host_passwd)
        self._local_time = datetime.date.today()

    def _create_mail(self, subject:str, to_address:str):
        mail = MIMEMultipart()
        mail["From"] = self._host_email_address
        mail["To"] = to_address
        mail["Subject"] = subject
        return mail
    
    def _add_file(self, mail: MIMEMultipart, file:str, type:str):
        with open(file, 'rb') as fp:
            attach_file = MIMEBase('application', "octet-stream")
            attach_file.set_payload(fp.read())
        encoders.encode_base64(attach_file)
        attach_file.add_header('Content-Disposition', 'attachment', filename=f"{self._local_time}_{type}_signal.csv")
        mail.attach(attach_file)

    def send(self, to_address, file):
        mail = self._create_mail(f"Monitor Report {self._local_time}", to_address)
        contents = "This is signals report"
        mail.attach(MIMEText(contents))
        self._add_file(mail, file+"/long_signal.csv", "long")
        self._add_file(mail, file+"/short_signal.csv", "short")
        status = self._smtp.sendmail(self._host_email_address, to_address, mail.as_string())

        return status
