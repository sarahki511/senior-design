from flask import Flask, redirect, url_for, render_template, request, send_from_directory, send_file
# import zipfile
# import subprocess
# from app import forms
from app import tools
from werkzeug.utils import secure_filename
import os, sys, shutil, zipfile, subprocess
# import sys
from app import app
from flask.helpers import flash
from datetime import datetime
# import shutil
# import smtplib

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
	ext = "txt, csv, hist, fa, fq, fastq, fna, fasta"
	if request.method == 'POST':
		if 'folder' not in request.files:
			print("is it here?")
			flash('No directory', 'error')
			return redirect(request.url)
		timestamp = datetime.now().strftime('%Y-%m-%d_%H%M%S')
		print(request.files.getlist('folder'))


		hasHist = False
		hasMapping = False
		
		#making the input and output directory 
		input_dir = os.path.join(app.config['IMAGE_UPLOADS'],'respect',timestamp)
		if not os.path.exists(input_dir):
			os.makedirs(input_dir,exist_ok=True)
		output_dir = os.path.join(app.config['IMAGE_UPLOADS'],'respect',timestamp+'_results')
		if not os.path.exists(output_dir):
			os.makedirs(output_dir,exist_ok=True)

		#for all input files in the directory
		for file in request.files.getlist('folder'):
			# if no uploaded file
			if file.filename == '':
				flash('No selected file', 'error')
				tools.get_rid_of_folders(input_dir, output_dir)
				return redirect(request.url)
			#check for file format
			if file and allowedFile(file.filename):
				
				#checking if there's a histogram file
				if file.filename.rsplit('.',1)[1].lower() == 'hist':
					hasHist = True
				filename = secure_filename(file.filename)
				print(filename)
				uploaded = os.path.join(input_dir, filename)
				file.save(uploaded)
				print(filename)
			# if extension is not acceptable
			else:
				flash("Unacceptable extension. Only accept: {}".format(ext + " and .gz version"), 'warning')
				tools.get_rid_of_folders(input_dir, output_dir)
				return redirect(request.url)
				

	   ## for histogram info file
		if (hasHist):
			if 'hist-file' not in request.files: 
			   flash('No file part', 'error')
			   tools.get_rid_of_folders(input_dir, output_dir)
			   return redirect(request.url)
			h_file = request.files['hist-file']
			# if no uploaded histogram info file
			if h_file.filename == '':
				print("Need Histogram Info File")
				flash('No file uploaded')
				tools.get_rid_of_folders(input_dir, output_dir)
				return redirect(request.url)
			# if there is an input file and the file extension is acceptable
			if h_file and allowedFile(h_file.filename):
				hist_info_filename = secure_filename(h_file.filename)
				hist_file_path = os.path.join(input_dir, hist_info_filename)
				h_file.save(hist_file_path)
				print(hist_info_filename + ' saved as histogram info file')
			# if exension is not acceptable
			else:
				flash("Unacceptable extension. Only accept: {}".format(ext + " and .gz version"), 'warning')
				tools.get_rid_of_folders(input_dir, output_dir)
				return redirect(request.url)

		##for mapping file
		if 'mapping-file' in request.files:
			m_file = request.files['mapping-file']
			# if mapping file is accepted
			if m_file.filename != '' and allowedFile(m_file.filename):
				hasMapping = True
				mapping_filename = secure_filename(m_file.filename)
				mapping_file_path = os.path.join(input_dir, mapping_filename)
				m_file.save(mapping_file_path)
				print(mapping_filename + ' saved as mapping file')
			# if file format is not accepted
			elif m_file.filename != '':
				flash("Unacceptable extension. Only accept: {}".format(ext + " and .gz version"), 'warning')
				tools.get_rid_of_folders(input_dir, output_dir)
				return redirect(request.url)
		kmer_size = request.form.get('kmer_size')
		num_iter = request.form.get('iter')
		if num_iter == '' or 'None':
			num_iter = "1000"
		temp = request.form.get('temp')
		if temp == '' or 'None':
			temp = "1.0"
		uniq = request.form.get('uniq')
		if uniq == '' or 'None':
			uniq = "0.1"
		norm = request.form.get('norm')
		if norm == '' or 'None':
			norm = "1"
		spec_num = request.form.get('spec-num')
		if spec_num == '' or 'None':
			spec_num = "50"
		print(num_iter + temp + uniq + norm + spec_num)
		#passing over to shell command
		# only for testing data we use -N 10, if it was published, we need to get the input from form
		if((hasHist == False) and (hasMapping == False)):
			c = "respect -d {0} -N 10 --debug -o {1}  -k {2} -T {3} -r {4} -l {5} -n {6}".format(input_dir,output_dir,\
				kmer_size, temp, uniq, norm, spec_num)
		elif ((hasHist == True) and (hasMapping == False)): 
			c = "respect -d {0} -I {1} -N 10 --debug -o {2} -k {3} -T {4} -r {5} -l {6} -n {7}".format(input_dir,hist_file_path, output_dir,\
				kmer_size, temp, uniq, norm, spec_num)
		elif ((hasHist == False) and (hasMapping == True)): 
			c = "respect -d {0} -m {1} -N 10 --debug -o {2} -k {3} -T {4} -r {5} -l {6} -n {7}".format(input_dir,mapping_file_path, output_dir,\
				kmer_size, temp, uniq, norm, spec_num)
		else: 
			c = "respect -d {0} -m {1} -I {2} -N 10 -k {3} -T {4} -r {5} -l {6} -n {7} --debug -o {8}".format(input_dir,mapping_file_path, \
				hist_file_path, kmer_size, temp, uniq, norm, spec_num, output_dir)
		print(c)
		# return redirect(request.url)
		#runs respect
		run_command(c)
		# delete input folder (and all files in directory)
		try:
			shutil.rmtree(input_dir)
		except OSError as e:
			print("Error: %s : %s" % (input_dir, e.strerror))
		flash("Successfully Uploaded Files! This might take a while. You can safely exit out of this page", "info")
		# send email when the respect is done running
		email = request.form.get('userEmail')
		getResultdir = 'respect/'+timestamp+'_results'
		tools.sendEmail(timestamp, email, output_dir, getResultdir)
		
		return redirect(url_for("result", result_dir = getResultdir))

	return render_template("respect.html", title = "RESPECT", id = "respect")
	
# link for skmer
# upload and run code for respect
@app.route("/skmer", methods=('GET', 'POST')) 
def skmer():
	ext = "txt, csv, hist, fa, fq, fastq, fna, fasta"
	if request.method == 'POST':
		if 'folder' not in request.files:
			flash('No directory', 'error')
			return redirect(request.url)
		timestamp = datetime.now().strftime('%Y-%m-%d_%H%M%S')
		print(request.files.getlist('folder'))

		#making the input and output directory 
		input_dir = os.path.join(app.config['IMAGE_UPLOADS'],'skmer',timestamp)
		if not os.path.exists(input_dir):
			os.makedirs(input_dir,exist_ok=True)
		output_dir = os.path.join(app.config['IMAGE_UPLOADS'],'skmer',timestamp+'_results')
		if not os.path.exists(output_dir):
			os.makedirs(output_dir,exist_ok=True)

		for file in request.files.getlist('folder'):
			# if no uploaded file
			if file.filename == '':
				flash('No selected file', 'error')
				tools.get_rid_of_folders(input_dir, output_dir)
				return redirect(request.url)
			#check for file format
			if file and allowedFile(file.filename):
				#uploads the files to uploads/skmer
				filename = secure_filename(file.filename)
				uploaded = os.path.join(input_dir, filename)
				file.save(uploaded)
				print(filename)
				# if extension is not acceptable
			else:
				flash("Unacceptable extension. Only accept: {}".format(ext + " and .gz version"), 'warning')
				tools.get_rid_of_folders(input_dir, output_dir)
				return redirect(request.url)

		librarydir = os.path.join(output_dir,'processed_library')
		dist_matrix_prefix = os.path.join(output_dir,'ref-dist-mat')
		c = "skmer reference {0} -l {1} -o {2} ".format(input_dir,librarydir,dist_matrix_prefix)
		
		#runs skmer 
		run_command(c)
		try:
			shutil.rmtree(input_dir)
		except OSError as e:
			print("Error: %s : %s" % (input_dir, e.strerror))
		flash("Successfully Uploaded Files! This might take a while. You can safely exit out of this page", "info")
		# send email when the respect is done running
		email = request.form.get('userEmail')
		getResultdir = 'skmer/'+timestamp+'_results'
		# tools.sendEmail(timestamp, email, output_dir, getResultdir)
		return redirect(url_for("result", result_dir = getResultdir))


	return render_template("skmer.html", title = "SKMER", id = "skmer")


# generate a result url -> display after done running a tool
@app.route("/result/<path:result_dir>")
def result(result_dir):
	# link = url_for('result', result_dir=result_dir, _external= True)
	# tools.sendEmail(timestamp, email, output_dir, result_dir)]
	output_dir = os.path.join(app.config['IMAGE_UPLOADS'], result_dir)
	return render_template("results.html", title = "RESULT", id = "result", name = output_dir + "/")


#make and return zip file	
@app.route("/return_files/<path:dirname>", methods=('GET', 'POST'))
def return_files(dirname):
	try:
		#getting absolute path to results folder 
		results_dir = os.path.join(os.getcwd(), dirname)
		
		# zip_path = os.path.join(results_dir,'output.zip')
		# zipf = zipfile.ZipFile(zip_path,'w', zipfile.ZIP_DEFLATED)
		# files = os.listdir(results_dir)
		# for root,dirs,files in os.walk(results_dir):
		# 	for file in files:
		# 		zipf.write(dirname+file)
		# zipf.close()

		shutil.make_archive(os.path.join(results_dir,'output'), 'zip', results_dir)

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
	# '.' in filename and \
	# 	(filename.rsplit('.',1)[1].lower() in app.config['ALLOWED_EXTENSIONS']) \
	# 		# or filename.rsplit('.')[1].lower() + ".gz" in app.config['ALLOWED_EXTENSIONS'] )

def run_command(command):
	# return 'Hello World'
	try:
		result = subprocess.check_output([command],shell=True)
		return result
	except subprocess.CalledProcessError as e:
		print( "error occurred")
		flash('Sub Process Error')
		return str(e)