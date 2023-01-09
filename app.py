from re import DEBUG, sub
from flask import Flask, render_template, request, redirect, send_file, url_for

import os
from werkzeug.utils import secure_filename
from werkzeug.datastructures import  FileStorage
import subprocess

app = Flask(__name__)


uploads_dir = os.path.join(app.instance_path, 'uploads')

os.makedirs(uploads_dir, exist_ok=True)

@app.route("/")
def hello_world():
    return render_template('index.html')


@app.route("/detect", methods=['POST'])
def detect():
    if not request.method == "POST":
        return
    video = request.files['video']
    video.save(os.path.join(uploads_dir, secure_filename(video.filename)))
    print(video)
    
    subprocess.run(['python', 'detect.py', '--source', os.path.join(uploads_dir, secure_filename(video.filename))],shell=True)

    # return os.path.join(uploads_dir, secure_filename(video.filename))
    obj = secure_filename(video.filename)
    return obj

@app.route("/opencam", methods=['GET'])
def opencam():
    print("here")
    subprocess.run(['python', 'detect.py', '--source', '0'])
    return "done"
    

@app.route('/return-files', methods=['GET'])
def return_file():
    obj = request.args.get('obj')
    loc = os.path.join("runs/detect", obj)
    print(loc)
    try:
        return send_file(os.path.join("runs/detect", obj), attachment_filename=obj)
        # return send_from_directory(loc, obj)
    except Exception as e:
        return str(e)


@app.after_request
def add_header(response):
    response.headers["Cache-Control"]="no-cache,no-store,must-revalidate"
    response.headers["Pragma"]="no-cache"
    response.headers["EXpires"]="0"
    response.headers["Cache-Control"]='public,max-age=0'
    return response

# @app.route('/display/<filename>')
# def display_video(filename):
# 	print('display_video filename: ' + filename)
# 	return redirect(url_for('static/God of War 2022.03.06 - 19.48.51.04', code=200))

# @app.route('/mask_rcnn' methods=['GET']):
# def mask_rcnn():
#     print("here")
#     subprocess.run(['python','mask.py','--source','0'])
#     return "done"