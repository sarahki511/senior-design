from flask import Flask, redirect, url_for, render_template, request, send_from_directory, send_file
import zipfile
import subprocess
# from app import forms
from app import tools
from werkzeug.utils import secure_filename
import os
import sys
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
			name = request.form.get('getUserName')
			tools.sendEmail(timestamp, email)
			return redirect(url_for('pending'))
			# return uploaded_file(filename)
	return render_template("consult.html", title = "CONSULT", id = "consult")

	
# link for respect
# upload and run code for respect
@app.route("/respect", methods=('GET', 'POST')) 
def respect():
	if request.method == 'POST':
		if 'folder' not in request.files:
			print("is it here?")
			flash('No file part')
			return redirect(request.url)
		timestamp = datetime.now().strftime('%Y-%m-%d_%H%M%S')
		print(request.files.getlist('folder'))


		hasHist = False
		hasMapping = False


		for file in request.files.getlist('folder'):
			# if no uploaded file
			if file.filename == '':
				flash('No selected file')
				return redirect(request.url)
			#check for file format
			if file and allowedFile(file.filename):
				if not os.path.exists(timestamp):
					os.makedirs(os.path.join(app.config['IMAGE_UPLOADS'],timestamp),exist_ok=True)
				#checking if there's a histogram file
				if file.filename.rsplit('.',1)[1].lower() == 'hist':
					hasHist = True
				filename = secure_filename(file.filename)
				uploaded = os.path.join(app.config['IMAGE_UPLOADS'],timestamp, filename)
				file.save(uploaded)
				print(filename)
				

	   ## for histogram info file
		if (hasHist):
			if 'hist-file' not in request.files: 
			   flash('No file part')
			   return redirect(request.url)
			h_file = request.files['hist-file']
			# if no uploaded histogram info file
			if h_file.filename == '':
				print("Need Histogram Info File")
				flash('No file uploaded')
				return redirect(request.url)
			if h_file and allowedFile(h_file.filename):
				hist_info_filename = secure_filename(h_file.filename)
				uploaded = os.path.join(app.config['IMAGE_UPLOADS'],timestamp, hist_info_filename)
				h_file.save(uploaded)
				print(hist_info_filename + ' saved as histogram info file')
		##for mapping file
		if 'mapping-file' in request.files:
			m_file = request.files['mapping-file']
			if m_file.filename != '' and allowedFile(m_file.filename):
				hasMapping = True
				mapping_filename = secure_filename(m_file.filename)
				uploaded = os.path.join(app.config['IMAGE_UPLOADS'],timestamp, mapping_filename)
				m_file.save(uploaded)
				print(mapping_filename + ' saved as mapping file')
		#making outputs folder
		if not os.path.exists(timestamp+'_results'):
			os.makedirs(os.path.join(app.config['IMAGE_UPLOADS'],timestamp+'_results'),exist_ok=True)
		
		input_dir = os.path.join(app.config['IMAGE_UPLOADS'],timestamp)
		output_dir = os.path.join(app.config['IMAGE_UPLOADS'],timestamp+'_results/')

		#passing over to shell command
		if((hasHist == False) and (hasMapping == False)):
			c = "respect -d {0} -N 10 --debug -o {1}".format(input_dir,output_dir)
		elif ((hasHist == True) and (hasMapping == False)): 
			c = "respect -d {0} -I {1} -N 10 --debug -o {2}".format(input_dir,input_dir+'/'+hist_info_filename, output_dir)
		elif ((hasHist == False) and (hasMapping == True)): 
			c = "respect -d {0} -m {1} -N 10 --debug -o {2}".format(input_dir,input_dir+'/'+mapping_filename, output_dir)
		else: 
			c = "respect -d {0} -m {1} -I {2} -N 10 --debug -o {3}".format(input_dir,input_dir+'/'+mapping_filename, input_dir+'/'+hist_info_filename ,output_dir)
		
		#runs respect
		run_respect(c)
		email = request.form.get('userEmail')
		getResultdir = timestamp+'_results'
		tools.sendEmail(timestamp, email, output_dir, getResultdir)
		
		# return result(output_dir, getResultdir)
		return redirect(url_for("result", result_dir = getResultdir))
		# return render_template("results.html", title = "RESULT", id = "result", name = output_dir)
		# return redirect(url_for('run_respect', command=c))
		# return redirect(url_for('pending'))
		# return redirect(url_for('download_file', name=filename))
	return render_template("respect.html", title = "RESPECT", id = "respect")
	# 

@app.route("/result/<result_dir>")
# def result(output_dir, result_dir):
def result(result_dir):
	# link = url_for('result', result_dir=result_dir, _external= True)
	# tools.sendEmail(timestamp, email, output_dir, result_dir)]
	output_dir = os.path.join(app.config['IMAGE_UPLOADS'], result_dir)
	return render_template("results.html", title = "RESULT", id = "result", name = output_dir)

def run_respect(command):
	# return 'Hello World'
	try:
		result = subprocess.check_output([command],shell=True)
		return result
	except subprocess.CalledProcessError as e:
		print( "error occurred")
		flash('Sub Process Error')
		return str(e)
	
@app.route("/return_files/<path:dirname>", methods=('GET', 'POST'))
def return_files(dirname):
	try:
		#getting absolute path to results folder 
		results_dir = os.path.join(os.getcwd(), dirname)
		zip_path = os.path.join(results_dir,'output.zip')

		zipf = zipfile.ZipFile(zip_path,'w', zipfile.ZIP_DEFLATED)
		files = os.listdir(results_dir)
		for file in files:
			zipf.write(dirname+file)

		# for root,dirs,files in os.walk(results_dir):
		# 	for file in files:
		# 		zipf.write(dirname+file)
		zipf.close()
		return send_from_directory(directory = results_dir,filename='output.zip',
				mimetype = 'zip',
				attachment_filename= 'output.zip',
				as_attachment = True)
	except Exception as e:
		return str(e)
	


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