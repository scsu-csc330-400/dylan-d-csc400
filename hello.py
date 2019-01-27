import os

from flask_wtf.file import FileRequired, FileAllowed

import graph_test

from flask import Flask, flash, render_template, request, send_file, jsonify, url_for
from flask_wtf import FlaskForm
from werkzeug.utils import secure_filename, redirect
from wtforms import SelectField, TextField, FileField, RadioField

import db

UPLOAD_FOLDER = './/upload'
ALLOWED_EXTENSIONS = {'xls', 'xlsx'}

app = Flask(__name__)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key = 'super secret key'


class GenForm(FlaskForm):
    CRN = SelectField('CRN', choices=[])
    semester = SelectField('semester', choices=[])
    exam = SelectField('exam', choices=[])
    type = RadioField('type', choices=[(1, 'By Exam'), (2, 'By Class'), (3, 'Normal')], default=1)
    color_passive = SelectField('color_passive', choices=[('r', 'Red'), ('g', 'Green'), ('b', 'Blue'),
                                                          ('c', 'Cyan'), ('m', 'Magenta'), ('y', 'Yellow'),
                                                          ('k', 'Black')])

    color_active = SelectField('color_active', choices=[('r', 'Red'), ('g', 'Green'), ('b', 'Blue'),
                                                        ('c', 'Cyan'), ('m', 'Magenta'), ('y', 'Yellow'),
                                                        ('k', 'Black')], default='b')

    upload = FileField('upload', validators=[
        FileRequired(),
        FileAllowed(['xls', 'xlsx'], 'Excel files only!')
    ])


class AddClassForm(FlaskForm):
    CRN = TextField('CRN')
    class_name = TextField('class_name')
    class_num = TextField('class_num')
    semester = TextField('class_num')


class AddExamForm(FlaskForm):
    class_id = SelectField('class_id', choices=[])


@app.route('/', methods=['GET', 'POST'])
def index():
    form = GenForm()

    conn = db.db_conn()
    cursor = conn.cursor()
    cursor.execute("SELECT DISTINCT semester FROM Class")
    semesters = cursor.fetchall()
    conn.close()
    cursor.close()

    form.semester.choices = [("", "---")] + [(semesters[0], semesters[0]) for semesters in semesters]
    form.CRN.choices = [("", "---")]
    form.exam.choices = [("", "---")]

    class_id = form.CRN.data
    exam = form.exam.data
    color_passive = form.color_passive.data
    color_active = form.color_active.data
    graph_type = form.type.data

    filename = ''
    if form.validate_on_submit():
        upload = form.upload.data
        filename = secure_filename(upload.filename)
        upload.save(os.path.join(app.instance_path, 'upload', filename))
        return redirect(url_for('index'))

    if request.method == 'POST':
        if form.semester.data is "" or form.CRN.data is "" or form.exam.data is "":
            flash("Select values before generating a graph", "cat1")
        else:
            if graph_type == '1':
                filename = graph_test.test1(class_id)
                # return send_file(".//graphs//BIO " + class_id + ".png", mimetype='image/png')
            elif graph_type == '2':
                flash("Under construction", "cat1")
            elif graph_type == '3':
                filename = graph_test.test(exam, class_id, color_passive, color_active)
                # return send_file(".//graphs//BIO " + class_id + ".png", mimetype='image/png')
    print(filename)
    return render_template('index.html', form=form, heading="Analyze", filename=filename)


@app.route('/edit', methods=['GET', 'POST'])
def edit():
    add_class_form = AddClassForm()
    CRN = add_class_form.CRN.data
    class_name = add_class_form.class_name.data
    class_num = add_class_form.class_num.data
    semester = add_class_form.semester.data

    add_exam_form = AddExamForm()
    conn = db.db_conn()
    cursor = conn.cursor()
    cursor.execute("SELECT class_id FROM Class")
    class_ids = cursor.fetchall()
    class_id = add_exam_form.class_id.data
    add_exam_form.class_id.choices = [("", "---")] + [(class_ids[0], class_ids[0]) for class_ids in class_ids]

    if "add_class" in request.form:
        if CRN is "" or class_name is "" or class_num is "" or semester is "":
            flash("Input error", "cat1")
        else:
            cursor.execute(
                "INSERT INTO Class (CRN, class_name, class_num, semester)"
                "VALUES('{}', '{}', '{}', '{}')".format(CRN, class_name, class_num, semester))
            conn.commit()
            cursor.execute(
                "SELECT class_id FROM Class WHERE CRN = '{}' AND class_name = '{}' AND class_num = '{}' AND semester "
                "= '{}'".format(
                    CRN, class_name, class_num, semester))
            class_id = cursor.fetchall()
            cursor.close()
            conn.close()
            flash("New Class ID: {}".format(class_id[0][0]), "cat1")

    elif "add_exam" in request.form:
        if class_id is "":
            flash("Input error", "cat1")
        else:
            cursor.execute("SELECT exam_num FROM Exam WHERE class_id = '{}'".format(
                class_id))
            exam_nums = cursor.fetchall()
            exam_num = 1
            if len(exam_nums) is not 0:
                exam_num = exam_nums[-1][0] + 1

            cursor.execute("INSERT INTO Exam (class_id, exam_num) VALUES('{}', '{}')".format(class_id,
                                                                                             exam_num))
            cursor.execute("SELECT exam_id FROM Exam WHERE class_id = '{}' AND exam_num = '{}'".format(
                class_id, exam_num))
            exam_id = cursor.fetchall()
            flash("New Exam ID: {}".format(exam_id[0][0]), "cat1")
            conn.commit()
            conn.close()
            cursor.close()
    conn.close()
    cursor.close()
    return render_template('edit.html', add_class_form=add_class_form, add_exam_form=add_exam_form, heading="Edit")


@app.route('/CRN/<semester>')
def get_crn(semester):
    conn = db.db_conn()
    cursor = conn.cursor()
    cursor.execute("SELECT class_id, CRN FROM Class Where semester = '" + semester + "';")
    CRNs = cursor.fetchall()
    conn.close()
    cursor.close()
    CRN_Array = []

    for CRN in CRNs:
        CRN_Obj = {'class_id': CRN[0], 'CRN': CRN[1]}
        CRN_Array.append(CRN_Obj)

    return jsonify({'CRNs': CRN_Array})


@app.route('/test/<class_id>')
def get_test(class_id):
    conn = db.db_conn()
    cursor = conn.cursor()
    cursor.execute(
        "select DISTINCT exam_id, exam_num from Exam INNER JOIN Class ON Class.class_id = Exam.class_id WHERE "
        "Class.class_id = " + class_id)
    tests = cursor.fetchall()
    print(tests)
    conn.close()
    cursor.close()
    testsArray = []

    for test in tests:
        testObj = {'exam_id': test[0], 'exam_num': test[1]}
        testsArray.append(testObj)

    return jsonify({'tests': testsArray})


@app.route('/class_submit', methods=['GET', 'POST'])
def class_submit():
    class_name = request.form.get('class_name')
    class_num = request.form.get('class_num')
    semester = request.form.get('semester')
    if not (class_name or class_num or semester):
        flash("Input error!", "cat1")
        return render_template('add_class.html')
    else:
        print(class_name, class_num, semester)
        connect = db.db_conn()
        cur = connect.cursor()
        cur.execute(
            "INSERT INTO Class (class_name, class_num, semester) VALUES('" + class_name + "', '" + class_num + "', '" + semester + "');")
        connect.commit()
        cur.close()
        connect.close()
        flash("Added Class", "cat1")
        return render_template('index.html')


@app.errorhandler(404)
def page_not_found(e):
    # note that we set the 404 status explicitly
    return render_template('404.html'), 404
