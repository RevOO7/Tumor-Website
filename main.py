import time
import json
import os
import main1
import main2
from flask import Flask, flash, request, redirect, url_for, render_template, Session
from werkzeug.utils import secure_filename
import numpy
import matplotlib.pyplot as plt
from io import BytesIO
import base64

i=1
j=2
UPLOAD_FOLDER = 'uploads/'
UPLOAD_CHEST_FOLDER = 'uploader/'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'mha'])

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

app = Flask(__name__)
app.secret_key = 'some_secret'
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 1


app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.after_request
def add_header(response):
    # response.cache_control.no_store = True
    response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, post-check=0, pre-check=0, max-age=0'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '-1'
    return response

@app.route("/")
def home():
	return render_template("index.html")

@app.route("/brain/results")
def results():
    time.sleep(5)
    figfile = BytesIO()
    plt.savefig(figfile, format='png')
    figfile.seek(0)
    figdata_png = base64.b64encode(figfile.getvalue())
    ### Remove b' from begining and ' in the end
    ### So that we can send the string within base64 noation
    result = str(figdata_png)[2:-1]
    return render_template('abc.html', result=result)



@app.route("/brain")
def brain():
        return render_template('elements.html')

@app.route("/handleUpload", methods=['POST'])
def handleFileUpload():
    print('chal ja bhai')
    # check if the post request has the file part
    if 'file' not in request.files:
        flash('No file part')
        return redirect(request.url)
    file = request.files['file']
    print('request.files', request.files)
    filename = secure_filename(file.filename)
    file.save(os.path.join(app.config['UPLOAD_FOLDER'], str(i)+ ".mha"))

    if main1.main1():
        time.sleep(5)
        time.sleep(10)
        return redirect(url_for('results'))
    
    else:
        print('nahi hua')
        return redirect(url_for('brain'))




@app.route("/chest/")
def chest():
		return render_template('generic.html')

@app.route("/handleChestUpload", methods=['POST'])
def handleChestUpload():
    # check if the post request has the file part
    if 'file' not in request.files:
        flash('No file part')
        return redirect(request.url)
    file = request.files['file']
    print('request.files', request.files)
    filename = secure_filename(file.filename)
    file.save(os.path.join('uploader', str(j)+ ".png"))

    res = main2.main2() 

    if res != "":
        time.sleep(5)
        time.sleep(5)
        return render_template('xyz.html', name = res)
   
    else:
        return redirect(url_for('chest'))



if __name__ == "__main__":
	app.run(host='127.0.0.1', port=5001, debug=True)