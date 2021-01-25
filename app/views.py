from flask import Flask, redirect, url_for, render_template, request
# from app import forms
from app import tools
from werkzeug.utils import secure_filename
import os
from app import app
from flask.helpers import flash
from datetime import datetime
import shutil
import smtplib
# import locAL3 as lc3
# import xAndyPlot as xyPlot

# home page -> render index.html
@app.route("/") 
def home():
    return render_template("index.html", title = "HOME", id = "home")

# link for consult
# upload and run code for consult
@app.route("/consult", methods=('GET', 'POST')) 
def consult():
    if request.method == 'POST':
        # if file does not exist in request.files
        if 'file' not in request.files:
            print("is it here?")
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if no uploaded file
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowedFile(file.filename):
            timestamp = datetime.now().strftime('%Y-%m-%d_%H%M%S')
            filename = secure_filename(file.filename)
            uploaded = os.path.join(app.config['IMAGE_UPLOADS'], timestamp)
            file.save(uploaded)
            email = request.form.get('userEmail')
            tools.sendEmail(timestamp, email)
            return redirect(url_for('pending'))
            # return uploaded_file(filename)
    return render_template("consult.html", title = "CONSULT", id = "consult")
    
# link for respect
# upload and run code for respect
@app.route("/respect", methods=('GET', 'POST')) 
def respect():
    # return getForm("respect")
    return render_template("respect.html", title = "RESPECT", id = "respect")
    

@app.route("/apples", methods=('GET', 'POST')) 
def apples():
    # return getForm("apples")
    return render_template("apples.html", title = "APPLES", id = "apples")

@app.route("/misa", methods=('GET', 'POST')) 
def misa():
    # return getForm("misa")
    return render_template("misa.html", title = "MISA", id = "misa")

@app.route("/pending", methods = ('GET', 'POST')) 
def pending():
    return render_template("pending.html", title = "PENDING", id = "pending")

def getForm(currentPg):
    form = forms.inputForm()
    htmlLink = currentPg + ".html"
    if form.validate_on_submit():
        # folderDir = os.path.join(os.path.dirname(app.instance_path), 'static','assets' )
        seqFile = form.sequenceFile.data
        fileName = secure_filename(seqFile.filename)
        seqFile.save(os.path.join(uploads_dir, fileName))
        flash('Document uploaded successfully!')
        return redirect("pending.html")
    return render_template(htmlLink, title = currentPg.upper(), id = currentPg, form = form)\

# return true or false
def allowedFile(filename):
    # if the filename has '.' and the word after the '.' 
    # is in allowedExtension -> return true
    return '.' in filename and \
        filename.rsplit('.',1)[1].lower() in app.config['ALLOWED_EXTENSIONS']