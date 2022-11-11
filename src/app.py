from flask import Flask, jsonify, request, Response
from flask_pymongo import PyMongo
from bson import json_util
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from bson.objectid import ObjectId


app = Flask(__name__)

app.secret_key = generate_password_hash("APIMongoPythonFlaskMonitoreo")
app.config["MONGO_URI"] = "mongodb://localhost:27017/invernadero"
mongo = PyMongo(app)


@app.route('/api/v1/addDatos', methods=['POST'])
def post_addDatos():
    print(request.json)
    datos = request.json
    if datos:
        id = mongo.db.datoCollection.insert_many(
            datos
        )
        print("estos son los datos --> ",str(id.inserted_ids))
        response = jsonify({
            '_id': str(id.inserted_ids),
        })
        response.status_code = 201
        return response
    else:
        return {'message': 'addDatos incorrectos'}

@app.route('/api/v1/datos', methods=['GET'])
def get_datos():
    datos = mongo.db.datoCollection.find()
    response = json_util.dumps(datos)
    return Response(response, mimetype="application/json")

@app.route('/api/v1/filterDatos', methods=['POST'])
def post_filterDatos():
    fecha_ini = request.json["fecha_ini"]
    fecha_fin = request.json["fecha_fin"]
    diccionario = {"FECHA": {"$gte": str(datetime.strptime(fecha_ini, "%Y-%m-%d")), "$lte": str(datetime.strptime(fecha_fin, "%Y-%m-%d"))}}
    print(diccionario)
    registros = mongo.db.datoCollection.find(diccionario)
    response = json_util.dumps(registros)
    #return jsonify(registros)
    return Response(response, mimetype="application/json")
    
@app.route('/api/v1/filterDatos/<fecha_ini>&<fecha_fin>', methods=['GET'])
def get_filterDatos(fecha_ini, fecha_fin):
    diccionario = {"FECHA": {"$gte": str(datetime.strptime(fecha_ini, "%Y-%m-%d")), "$lte": str(datetime.strptime(fecha_fin, "%Y-%m-%d"))}}
    print(diccionario)
    registros = mongo.db.datoCollection.find(diccionario)
    response = json_util.dumps(registros)
    response
    return Response(response, mimetype="application/json")

@app.route('/', methods=['GET'])
def main():
    return {'message': 'API YA ESTA ARRIBA INVERNADERO'}


if __name__ == ('__main__'):
    main()
    app.run(debug=True)
