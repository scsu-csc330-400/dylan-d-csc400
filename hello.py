from flask import Flask, render_template, request, send_file
import graph

app = Flask(__name__)


@app.route('/')
def my_form():
    return render_template('index.html')


@app.route('/', methods=['POST'])
def my_form_post():
    exam = request.form.get('exam')
    class_num = request.form.get('class_num')
    color_passive = request.form.get('color_passive')
    color_active = request.form.get('color_active')
    graph.make_graph(exam, class_num, color_passive, color_active)
    return send_file("BIO " + class_num + ".png", mimetype='image/png')
