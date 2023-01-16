# -*- coding: utf-8 -*-
from flask import Flask, render_template
import pandas as pd
import json
import matplotlib.pyplot as plt
from flask_wtf import FlaskForm
from wtforms import FileField, SubmitField
from werkzeug.utils import secure_filename
import os
import boto3
import time

app = Flask(__name__,template_folder="template")
app.config['SECRET_KEY'] = 'supersecretkey'
app.config['UPLOAD_FOLDER'] = 'static/files'

rutaprincipal = "static/files";
nombredearchivo = "/ejercicio1_b1.xlsx";
carga = pd.read_excel(rutaprincipal + nombredearchivo) #concatenar  rutas de base de datos
datos = pd.DataFrame(carga) # cargar los datos en un data frame
datos.head()
datos1 = datos.iloc[:,0:4]
datos2 = datos1.dropna(); ## Eliminar valores nan
base1 = datos2.drop_duplicates(subset=["id"]); # Eliminar valores repetidos
base1 = base1.iloc[:,1:4]
base2 = pd.read_table('static/files/ejercicio1_b2.txt',)
calculo = pd.DataFrame({'EDAD': [- int(base2.iloc[0,3][6:10]) + 2014, - int(base2.iloc[1,3][6:10]) + 2014, - int(base2.iloc[2,3][6:10]) + 2014, - int(base2.iloc[3,3][6:10]) + 2014, - int(base2.iloc[4,3][6:10]) + 2014, - int(base2.iloc[5,3][6:10]) + 2014]}) ##Calcula edad de los clientes
base2 = pd.concat([base2, calculo], axis = 1) ##Ingresar calculo a la base de datos
base2['NOMBRECOMPLETO'] = base2.NOMBRE.str.cat(base2.APELLIDO, sep=' ') ##Unir variable nombre con apellido
cruce = pd.merge(base2,base1, left_on="CEDULA", right_on="cc_cliente"); ## Cruzar base de datos con identificación del cliente
cruce = cruce.rename(columns={'numero de pedido':'PEDIDO'}) # Cambiar nombre de la columna
cruce = cruce.rename(columns={'Tipo de pedido':'TIPO'}) # Cambiar nombre de la columna
cruce["NOMBRECOMPLETO"]= cruce["NOMBRECOMPLETO"].str.capitalize(); # Convettir sólo primera letra en mayuscula
cruce = cruce.iloc[:,0:8]
result = cruce.to_json(orient="records")
parsed = json.loads(result) # Convertir archivo dataframe en formato JSON

# s3 = boto3.client("s3")
# client = boto3.client('s3',
#     aws_access_key_id='AKIARXJBCZERBOKSPFFF',
#     aws_secret_access_key='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',
# )

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
    return result
@app.route("/pedidos")
def datos():
    return render_template("pedidos.html", tabla = parsed, long = len(parsed))
@app.route("/graficos")
def grafi():
    plt.bar(cruce.iloc[:,5], cruce.iloc[:,6])
    x = plt.show()
    return render_template("graficos.html", x=x)
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)


