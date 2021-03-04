from app import app
import os
import smtplib, ssl, certifi
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from flask import Flask, url_for

def sendEmail(timestamp, email, output_dir, result_dir):
    # get developer's email address and pwd
    sendAddress = app.config['EMAIL_ID']
    sendPwd = app.config['EMAIL_PWD']
    # result files
    files = ["estimated-parameters.txt", "estimated-spectra.txt"]
    msg = MIMEMultipart()
    msg['To'] = email
    msg['From'] = sendAddress
    msg['Subject'] = 'Skmer: your results are ready'
    link = url_for("result",  result_dir=result_dir, _external= True)
    bodyInfo = "Dear User,\n We have succesfully ran the software.\n You can either visualize your results through this link: {}.\n\
        We have also attached the results in this email.\n".format(link)
    body = MIMEText(bodyInfo, 'html', 'utf-8')  
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