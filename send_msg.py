import smtplib
import settings
import json


def send_mail(msg:str):
    with open(settings.CRED_DIR, "+r") as file:
        data=json.load(file)

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(data['senders_mail'], data['senders_mail_password'])
    server.sendmail(data['senders_mail'], data['recivers_mail'], msg)
    server.quit()
