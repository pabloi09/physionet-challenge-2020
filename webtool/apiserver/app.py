from flask import Flask, flash, request, redirect, url_for, render_template, jsonify
from werkzeug.utils import secure_filename
import os
from classifier_interface import ClassifierInterface
import numpy as np
import json
from flask_cors import CORS, cross_origin

app = Flask(__name__, template_folder=".")
UPLOAD_FOLDER = '/home/pablo/projects/physionet-challenge-2020/webtool/apiserver/tmp'
ALLOWED_EXTENSIONS = {'mat', 'hea'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
cors = CORS(app, resources={r"/*": {"origins": "*"}})
classifier = ClassifierInterface()
app.secret_key = "super secret key"

def allowed_combination(filename1,filename2):
    if filename2.split(".")[0] == filename1.split(".")[0]:
        if (".hea" in filename1 and ".mat" in filename2) or (".hea" in filename2 and ".mat" in filename1):
            return allowed_file(filename2) and allowed_file(filename1)
        

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

	
@app.route('/', methods = ['POST','GET'])
@cross_origin()
def upload_file():
   response = {}
   if 'file1' not in request.files or 'file2' not in request.files:
       flash('No file part')
       return redirect(request.url)
   f1 = request.files['file1']
   f2 = request.files['file2']
   
   if f1.filename == '' or f2.filename == '':
       flash('No selected file')
       return redirect(request.url)
   if f1 and f2 and allowed_combination(f1.filename, f2.filename):
       filepath1 = os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(f1.filename))
       filepath2 = os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(f2.filename))
       
       f1.save(filepath1)
       f2.save(filepath2)
       
       if ".mat" in filepath1:
           current_label, current_score, real_out, leads, classes,fs = classifier.predict(filepath1)
       else:
           current_label, current_score, real_out, leads, classes,fs = classifier.predict(filepath2)
       
       os.remove(filepath2)
       os.remove(filepath1)
       
       response["leads"] = leads
       response["classes"] = classes.tolist()
       response["real_out"] = real_out.tolist()
       response["labels"] = current_label.tolist()
       response["score"] = current_score.tolist()
       response["fs"] = fs

   return jsonify(response)
		
if __name__ == '__main__':
   app.run(debug = True)