from flask import Flask, redirect, url_for, render_template
from app import forms
from app import tools
from werkzeug.utils import secure_filename
import os
from app import app
from flask.helpers import flash
import shutil
import smtplib
# import locAL3 as lc3
# import xAndyPlot as xyPlot


# app.config['SECRET_KEY'] = '\xd8\xf1\xa5\xdd\x8eD\xf7\xdf]\xe7\x05\xf79\xa3\x0e\xd1'
# uploads_dir = os.path.join(app.instance_path, 'uploads')
# os.makedirs(uploads_dir, exist_ok=True)

# Bootstrap(app)
@app.route("/") 
def home():
    return render_template("index.html", title = "HOME", id = "home")

@app.route("/consult", methods=('GET', 'POST')) 
def consult():
    # return getForm("consult")
    return render_template("consult.html", title = "CONSULT", id = "consult")
    

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
    return render_template(htmlLink, title = currentPg.upper(), id = currentPg, form = form)

# if __name__ == "__main__":
#     app.run(debug=True)