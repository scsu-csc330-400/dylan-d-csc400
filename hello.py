import os
from flask import Flask, flash, render_template, request, send_file
from werkzeug.utils import secure_filename
import graph
import sheet

UPLOAD_FOLDER = './/upload'
ALLOWED_EXTENSIONS = {'xls', 'xlsx'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key = 'super secret key'


@app.route('/')
def my_form():
    return render_template('index.html')


@app.route('/', methods=['POST'])
def my_form_post():
    exam = request.form.get('exam_gen')
    class_num = request.form.get('class_num_gen')
    color_passive = request.form.get('color_passive')
    color_active = request.form.get('color_active')
    graph.make_graph(exam, class_num, color_passive, color_active)
    return send_file(".//graphs//BIO " + class_num + ".png", mimetype='image/png')


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/verify', methods=['GET', 'POST'])
def verify():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file selected', 'cat1')
            return render_template('index.html')
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file', 'cat1')
            return render_template('index.html')
        if not allowed_file(file.filename):
            flash("Invalid file type", 'cat1')
            return render_template('index.html')
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            exam = request.form.get('exam_up')
            class_num = request.form.get('class_num_up')
            global result
            result = sheet.verify(filename, exam, class_num)
        return render_template('index.html')


@app.route('/upload', methods=['GET', 'POST'])
def upload():
    sheet.upload(result)
    return render_template('index.html')

