# Importing the libraries that are needed for the program to run.
from flask import Flask, jsonify, request, Response
from flask_pymongo import PyMongo
from bson import json_util
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from bson.objectid import ObjectId


# Creating a Flask application instance.
app = Flask(__name__)


# Setting the secret key for the Flask app and the MongoDB URI.
app.secret_key = generate_password_hash("APIMongoPythonFlaskMonitoreo")
app.config["MONGO_URI"] = "mongodb://localhost:27017/invernadero"


# Creating a connection to the MongoDB database.
mongo = PyMongo(app)


"""
    It takes a JSON object, inserts it into a MongoDB collection, and returns the ID of the inserted
    object.
    :return: The response is a JSON object with the _id of the inserted document.
"""
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


"""
    It takes a request, queries the database, and returns a response
    :return: A list of dictionaries.
"""
@app.route('/api/v1/datos', methods=['GET'])
def get_datos():
    datos = mongo.db.datoCollection.find()
    response = json_util.dumps(datos)
    return Response(response, mimetype="application/json")


"""
    It takes a JSON object with two fields, fecha_ini and fecha_fin, and returns a JSON object with all
    the documents in the collection that have a date between the two dates
    :return: A JSON object with the following structure:
    [
        "_id": {
            "": "5c9b8f8f8b0be816b8b8b8b8"
        },
        "FECHA": "2019-03-27",
        "HORA": "12:00:00",
        ...,
        ...
    ]
"""
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


"""
    It filters the data from the database by date.
    
    :param fecha_ini: 2020-01-01
    :param fecha_fin: 2020-01-01
    :return: The response is a JSON object with the data that is in the database.
"""
@app.route('/api/v1/filterDatos/<fecha_ini>&<fecha_fin>', methods=['GET'])
def get_filterDatos(fecha_ini, fecha_fin):
    diccionario = {"FECHA": {"$gte": str(datetime.strptime(fecha_ini, "%Y-%m-%d")), "$lte": str(datetime.strptime(fecha_fin, "%Y-%m-%d"))}}
    print(diccionario)
    registros = mongo.db.datoCollection.find(diccionario)
    response = json_util.dumps(registros)
    response
    return Response(response, mimetype="application/json")


"""
    It returns a JSON object with a message key and a value of "API YA ESTA ARRIBA INVERNADERO"
    :return: A dictionary with a key and value.
"""
@app.route('/', methods=['GET'])
def main():
    return {'message': 'API YA ESTA ARRIBA INVERNADERO'}


# Running the Flask app.
if __name__ == ('__main__'):
    main()
    app.run(host="0.0.0.0", port=5000, debug=True)
