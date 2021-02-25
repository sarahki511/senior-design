from app import app
import os
import smtplib, ssl, certifi
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication

def sendEmail(timestamp, email, output_dir):
    # get developer's email address and pwd
    sendAddress = app.config['EMAIL_ID']
    sendPwd = app.config['EMAIL_PWD']
    # result files
    files = ["estimated-parameters.txt", "estimated-spectra.txt"]
    msg = MIMEMultipart()
    msg['To'] = email
    msg['From'] = sendAddress
    msg['Subject'] = 'Skmer: your results are ready'
    body = MIMEText('Test results attached.', 'html', 'utf-8')  
    msg.attach(body)  # add message body (text or html)
    
    for f in files:  # add files to the message
        file_path = os.path.join(output_dir, f)
        attachment = MIMEApplication(open(file_path, "rb").read(), _subtype="txt")
        attachment.add_header('Content-Disposition','attachment', filename=f)
        msg.attach(attachment)
    # context = ssl.create_default_context()
    with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
            smtp.ehlo()
            # smtp.starttls(context=context)
            smtp.starttls()
            smtp.ehlo()
            smtp.login(sendAddress, sendPwd)
            # subject = 'Test if email sends'
            # body = f'sent!'
            # msg = f'Subject: {subject}\n\n{body}'
            smtp.sendmail(msg['From'], msg['To'], msg.as_string())
            smtp.close()
            print('email sent')