from app import app
import os, shutil
import smtplib, ssl, certifi
import subprocess, zipfile, re
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from flask import Flask, url_for, render_template
from email_validator import validate_email, EmailNotValidError

def sendResults(timestamp, email, output_dir, result_dir):
    # get developer's email address and pwd
    sendAddress = app.config['EMAIL_ID']
    sendPwd = app.config['EMAIL_PWD']
    # result files
    files = os.listdir(os.path.join(app.config['IMAGE_UPLOADS'],result_dir))
    msg = MIMEMultipart()
    msg['To'] = email
    msg['From'] = sendAddress
    msg['Subject'] = 'Skmer: your results are ready'
    link = url_for("result",  result_dir=result_dir, _external= True)
    print(link)
    body = MIMEText(render_template("email.html", link = link), 'html')  
    msg.attach(body)  # add message body (text or html)
    
    for f in files:  # add files to the message
        file_path = os.path.join(output_dir, f)
        attachment = MIMEApplication(open(file_path, "rb").read(), _subtype="txt")
        attachment.add_header('Content-Disposition','attachment', filename=f)
        msg.attach(attachment)
    try:
        with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
                smtp.ehlo()
                smtp.starttls()
                smtp.ehlo()
                smtp.login(sendAddress, sendPwd)
                smtp.sendmail(msg['From'], msg['To'], msg.as_string())
                smtp.close()
                print('email sent results')
    except:
        print("An error occurred")

def sendContact(firstN, lastN, user_email, user_msg):
    sendAddress = app.config['EMAIL_ID']
    sendPwd = app.config['EMAIL_PWD']
    msg = MIMEMultipart()
    msg['To'] = sendAddress
    # msg['To'] = user_email
    msg['From'] = sendAddress
    msg['Subject'] = "Contact Request from Skmer Website"
    body = MIMEText(render_template("email.html", link = '', firstN = firstN, \
        lastN = lastN, user_email = user_email, user_msg = user_msg), 'html')  
    msg.attach(body)
    try:
        with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
                smtp.ehlo()
                smtp.starttls()
                smtp.ehlo()
                smtp.login(sendAddress, sendPwd)
                smtp.sendmail(msg['From'], msg['To'], msg.as_string())
                smtp.close()
                print('email sent for contact')
    except:
        print("An error occurred")

def get_rid_of_folders(input_dir, output_dir):
	try:
		shutil.rmtree(input_dir)
		shutil.rmtree(output_dir)
	except OSError as e:
		print("Error: %s : %s" % (input_dir, e.strerror))

# return true or false
def allowedFile(filename):
	# if the filename has '.' and the word after the '.' 
	
	if '.' in filename:
		ext = filename.rsplit('.',1)[1].lower()
		upper = filename.rsplit('.',1)[0]
	# already invalid so return false
	else:
		return 0
	# if zipped, check if the ext is valid before gz
	if ext == "gz":
		return upper.rsplit('.',1)[1].lower() in app.config['ALLOWED_EXTENSIONS']
	# is in allowedExtension -> return true
	return ext in app.config['ALLOWED_EXTENSIONS']

def run_command(command):
	# return 'Hello World'
	try:
		result = subprocess.check_output([command],shell=True)
		return result
	except subprocess.CalledProcessError as e:
		print( "error occurred")
		flash('Sub Process Error')
		return str(e)