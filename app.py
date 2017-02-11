import os

import numpy
import pickle
import cv2

import sys

from flask import Flask, render_template, request, redirect, url_for, flash
from werkzeug.utils import secure_filename

#from flask.ext.sqlalchemy import SQLAlchemy

UPLOAD_FOLDER = '/tmp'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key = 'many random bytes'

#DATABASE_URL = os.environ.get('DATABASE_URL', 'sqlite:////tmp/flask_app.db')

#app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL
#db = SQLAlchemy(app)


# class User(db.Model):
#   id = db.Column(db.Integer, primary_key=True)
#   name = db.Column(db.String(100))
#   email = db.Column(db.String(100))

#   def __init__(self, name, email):
#     self.name = name
#     self.email = email

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

def findimg(time, img):
#    haarcscade = '/home/mona/Documents/2017Spring/AdvancedBigData/FacialExpression/opencv-3.2.0/data/haarcascades'
    face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
    imagePath = '/tmp/'
    image = cv2.imread(imagePath+img)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)
    roi_color = []
    for (x,y,w,h) in faces:
        roi_color.append(image[y:y+h, x:x+w])
    if len(roi_color) == 0:
        return 0

    hist = cv2.calcHist([roi_color[0]], [0, 1, 2], None, [8, 8, 8], [0, 256, 0, 256, 0, 256])
    hist = cv2.normalize(hist, hist).flatten()
    maxdist = 0
    maxnum = ''
    for im in images[time]:
        dist = cv2.compareHist(im[0], hist, cv2.HISTCMP_CORREL)
        if maxdist < dist:
            maxdist = dist
            maxnum = im[1]

    return maxnum

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html', person=person)


@app.route('/person', methods=['POST'])
def person():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename == '' or request.form['time'] == "":
            flash('No selected file')
            return redirect(url_for('index'))
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            time = request.form['time']
            person = findimg(int(time), filename)
            #print filename
            if person == 0:
                flash("No face detected")
                return redirect(url_for('index'))
            return render_template('index.html', person=person)
    return redirect(url_for('index'))

person = "who"
with open("test.txt", "rb") as fp:   # Unpickling
    images = pickle.load(fp)

if __name__ == '__main__':
    #port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', debug=True)

