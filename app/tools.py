from app import app
import subprocess
import os
import smtplib, ssl, certifi

def sendEmail(timestamp, email):
    sendAddress = app.config['EMAIL_ID']
    sendPwd = app.config['EMAIL_PWD']
    # context = ssl.create_default_context()
    with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
            smtp.ehlo()
            # smtp.starttls(context=context)
            smtp.starttls()
            smtp.ehlo()
            smtp.login(sendAddress, sendPwd)
            subject = 'Test if email sends'
            body = f'sent!'
            msg = f'Subject: {subject}\n\n{body}'
            smtp.sendmail(sendAddress, email, msg)
            print('email sent')