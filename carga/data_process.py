import pandas as pd
import json
import os
from carga.load_data import lambda_handler

def load_data():
    vector = lambda_handler('a','a')
    carga = pd.read_excel(vector[1]) #concatenar  rutas de base de datos
    datos = pd.DataFrame(carga) # cargar los datos en un data frame
    datos.head()
    datos1 = datos.iloc[:,0:4]
    datos2 = datos1.dropna(); ## Eliminar valores nan
    base1 = datos2.drop_duplicates(subset=["id"]); # Eliminar valores repetidos
    base1 = base1.iloc[:,1:4]
    vector = lambda_handler('a','a')
    base2 = pd.read_table(vector[0])
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
    return [parsed,cruce]
