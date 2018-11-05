from flask import Flask
from flask import jsonify
from flask import abort
from flask import make_response
from flask import request

app = Flask(__name__)

usuarios = [
	{'id':1,
	'nombreUsuario': 'David Gilmour',
    'age':40,
    'genre':0
	},
	{'id':2,
	'nombreUsuario': 'Richarda Wright',
    'age':60,
    'genre':1
	},
	{'id':3,
	'nombreUsuario': 'Roger Waters',
    'age':50,
    'genre':0
	}
]

diagnosticos = [
    {
    'id_user':1,
    'id_diag':1,
    'descripcion':"Pues está resfriado",
    'fecha':"18/7/2017"
    },
    {
    'id_user':2,
    'id_diag':2,
    'descripcion':"Está en coma",
    'fecha':"21/8/2017"
    },
    {
    'id_user':2,
    'id_diag':3,
    'descripcion':"Se ha despertado",
    'fecha':"23/8/2017"
    }
]

tratamientos = [
    {
    'id_diag':1,
    'id_tratamiento':1,
    'id_medicamento':1,
    'frecuencia':"1 vez al dia",
    'descripcion':"Con agua"
    },
    {
    'id_diag':2,
    'id_tratamiento':2,
    'id_medicamento':2,
    'frecuencia':"1 vez al mes",
    'descripcion':"Con agua"
    },
    {
    'id_diag':2,
    'id_tratamiento':3,
    'id_medicamento':0,
    'frecuencia':"",
    'descripcion':"reposo"
    }
]

medicamentos = [
    {
    'id_medicamento':0,
    'nombre':"Nada"
    },
    {
    'id_medicamento':1,
    'nombre':"Ibuprofeno"
    },
    {
    'id_medicamento':2,
    'nombre':"Fortasec"
    }
]

#Definimos la respuesta para el codigo de error 404
@app.errorhandler(404)
def not_found(error):
	return make_response(jsonify({'error': 'No encontrado'}),404)

@app.route('/')
def index():
    return "Bienvenido a la aplicación de gestion de usuarios del hospital"

@app.route('/v1/usuarios/', methods=['GET'])
def getUsuarios():
	return jsonify({'usuarios': usuarios})

@app.route('/v1/usuarios/<int:id>/', methods=['GET'])
def getUsuario(id):
    for usuario in usuarios:
        if usuario.get('id') == id:
            return jsonify({'usuarios':usuario})
    abort(404)

@app.route('/v1/usuarios/', methods=['POST'])
def crearUsuario():
    if not request.json or not 'email' in request.json:
        abort(404)
    id = usuarios[-1].get('id') + 1
    nombreUsuario = request.json.get('nombreUsuario')
    age = request.json.get('age')
    genre = request.json.get('genre')
    usuario = {'id': id, 'nombreUsuario': nombreUsuario, 'age': age, 'genre': genre}
    usuarios.append(usuario)
    return jsonify({'usuario':usuario}),201

@app.route('/v1/usuarios/<int:id>/', methods=['PUT'])
def actualizarUsuario(id):
	usuario = [usuario for usuario in usuarios if usuario['id'] == id]
	usuario[0]['nombreUsuario'] = request.json.get('nombreUsuario', usuario[0]['nombreUsuario'])
	usuario[0]['age'] = request.json.get('age', usuario[0]['age'])
	usuario[0]['genre'] = request.json.get('genre', usuario[0]['genre'])
	return jsonify({'usuarios':usuario[0]})

@app.route('/v1/usuarios/<int:id>/', methods=['DELETE'])
def borrarUsuario(id):
	usuario = [usuario for usuario in usuarios if usuario['id'] == id]
	usuarios.remove(usuario[0])
	return jsonify({}), 204 # No content

@app.route('/v1/usuarios/<int:id>/diagnosticos/',methods = ['GET'])
def getDiagnosticos(id):
    resultado = []
    for diagnostico in diagnosticos:
        if diagnostico.get('id_user') == id:
            resultado.append({'diagnosticos':diagnostico})
    return jsonify(resultado)



@app.route('/v1/usuarios/<int:id>/diagnosticos/<int:id_diag>/',methods = ['GET'])
def getDiagnostico(id,id_diag):
    for diagnostico in diagnosticos:
        if diagnostico.get('id_diag') == id_diag and diagnostico.get('id_user') == id:
            return jsonify({'diagnosticos':diagnostico})
    abort(404)

@app.route('/v1/usuarios/<int:id>/diagnosticos/<int:id_diag>/tratamientos/',methods = ['GET'])
def getTratamientos(id,id_diag):
    resultado = []
    for tratamiento in tratamientos:
        if tratamiento.get('id_diag') == id_diag and tratamiento.get('id_diag') == id_diag:
            resultado.append({'tratamientos':tratamiento})
    return jsonify(resultado)

@app.route('/v1/usuarios/<int:id>/diagnosticos/<int:id_diag>/tratamientos/<int:id_tratamiento>',methods = ['GET'])
def getTratamiento(id,id_diag,id_tratamiento):
    for tratamiento in tratamientos:
        if tratamiento.get('id_diag') == id_diag and tratamiento.get('id_tratamiento') == id_tratamiento:
            return jsonify({'tratamientos':tratamiento})
    abort(404)

@app.route('/v1/medicamentos/', methods=['GET'])
def getMedicamentos():
	resultado = []
	for medicamento in medicamentos:
		resultado.append({'medicamentos':medicamento})
	return jsonify(resultado)

@app.route('/v1/medicamentos/<int:id>/', methods=['GET'])
def getMedicamento(id):
    for medicamento in medicamentos:
        if medicamento.get('id_medicamento') == id:
            return jsonify({'medicamentos':medicamento})
    abort(404)

if __name__ == '__main__':
    app.run(debug=True)
