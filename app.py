# -*- coding: utf-8 -*-
from flask import Flask, render_template
import matplotlib.pyplot as plt
from flask_wtf import FlaskForm
from wtforms import FileField, SubmitField
from werkzeug.utils import secure_filename
import os
import boto3
import time
from carga.data_process import load_data
from carga.load_data import lambda_handler

app = Flask(__name__,template_folder="template")
app.config['SECRET_KEY'] = 'supersecretkey'
app.config['UPLOAD_FOLDER'] = 'static/files'
s3 = boto3.client("s3")

# s3.download_file(
#     Bucket="corpstudios", Key="stage_area/catalogos/OASIS_MST_CATEGORIA.csv", Filename="static/files/OASIS_MST_CATEGORIA.csv"
# )
class Uploadfile(FlaskForm):
    file = FileField("File")
    submit = SubmitField("Upload File")

@app.route("/", methods=['GET',"POST"])
def index():
    form = Uploadfile()
    if form.validate_on_submit():
        file = form.file.data
        print(file)
        try:
            file.save(os.path.join(os.path.abspath(os.path.dirname(__file__)),app.config['UPLOAD_FOLDER'],secure_filename(file.filename)))
            s3.upload_file(
                Filename="static/files/ejercicio1_b1.xlsx", Bucket="corpstudios", Key="stage_area/geografias_panama/nielsen_panama/input_files/ejercicio1_b1.xlsx")
        except FileNotFoundError as e:
            print('Suba por favor un archivo')
    return render_template("index.html",form=form)
@app.route("/api")
def get():
    vector = load_data()
    return vector[0]
@app.route("/pedidos")
def datos():
    vector = load_data()
    return render_template("pedidos.html", tabla = vector[0], long = len(vector[0]))
@app.route("/graficos")
def grafi():
    vector = load_data()
    plt.bar(vector[1].iloc[:,5], vector[1].iloc[:,6])
    x = plt.show()
    return render_template("graficos.html", x=x)
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)


