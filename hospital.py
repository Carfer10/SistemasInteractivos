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

#Definimos la respuesta para el codigo de error 404
@app.errorhandler(418)
def incorrect_params(error):
	return make_response(jsonify({'error': 'Valor invalido en campo de texto'}),418)

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
            return jsonify({'usuario':usuario})
    abort(404)

@app.route('/v1/usuarios/', methods=['POST'])
def crearUsuario():
    id = usuarios[-1].get('id') + 1
    nombreUsuario = request.json.get('nombreUsuario')
    if not nombreUsuario:
        abort(418)
    age = request.json.get('age')
    genre = request.json.get('genre')
    usuario = {'id': id, 'nombreUsuario': nombreUsuario, 'age': age, 'genre': genre}
    usuarios.append(usuario)
    return jsonify({'usuario':usuario}),201

@app.route('/v1/usuarios/<int:id>/', methods=['PUT'])
def actualizarUsuario(id):
	usuario = [usuario for usuario in usuarios if usuario['id'] == id]
	usuario[0]['nombreUsuario'] = request.json.get('nombreUsuario', usuario[0]['nombreUsuario'])
	if not usuario[0]['nombreUsuario']:
		abort(418)
	usuario[0]['age'] = request.json.get('age', usuario[0]['age'])
	usuario[0]['genre'] = request.json.get('genre', usuario[0]['genre'])
	return jsonify({'usuario':usuario[0]})

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
            resultado.append({'diagnostico':diagnostico})
    return jsonify(resultado)

@app.route('/v1/usuarios/<int:id>/diagnosticos/',methods = ['POST'])
def postDiagnostico(id):
	id_diag = diagnosticos[-1].get('id_diag') + 1
	descripcion = request.json.get('descripcion')
	if not descripcion:
		abort(418)
	fecha = request.json.get('fecha')
	diagnostico = {'id_diag': id_diag, 'descripcion': descripcion, 'fecha': fecha, 'id_user': id}
	diagnosticos.append(diagnostico)
	print("esto:{}".format(diagnostico))
	return jsonify({'diagnostico':diagnostico}),201

@app.route('/v1/usuarios/<int:id>/diagnosticos/<int:id_diag>/',methods = ['GET'])
def getDiagnostico(id,id_diag):
    for diagnostico in diagnosticos:
        if diagnostico.get('id_diag') == id_diag and diagnostico.get('id_user') == id:
            return jsonify({'diagnostico':diagnostico})
    abort(404)

@app.route('/v1/usuarios/<int:id>/diagnosticos/<int:id_diag>/',methods = ['PUT'])
def putDiagnostico(id,id_diag):
	diagnostico = [diagnostico for diagnostico in diagnosticos if diagnostico['id_diag'] == id_diag]
	diagnostico[0]['descripcion'] = request.json.get('descripcion', diagnostico[0]['descripcion'])
	if not diagnostico[0]['descripcion']:
		abort(418)
	diagnostico[0]['fecha'] = request.json.get('fecha', diagnostico[0]['fecha'])
	return jsonify({'diagnostico':diagnostico[0]})

@app.route('/v1/usuarios/<int:id>/diagnosticos/<int:id_diag>/', methods=['DELETE'])
def deleteDiagnostico(id,id_diag):
	diagnostico = [diagnostico for diagnostico in diagnosticos if diagnostico['id_diag'] == id_diag]
	diagnosticos.remove(diagnostico[0])
	return jsonify({}), 204 # No content

@app.route('/v1/usuarios/<int:id>/diagnosticos/<int:id_diag>/tratamientos/',methods = ['GET'])
def getTratamientos(id,id_diag):
    resultado = []
    for tratamiento in tratamientos:
        if tratamiento.get('id_diag') == id_diag and tratamiento.get('id_diag') == id_diag:
            resultado.append({'tratamiento':tratamiento})
    return jsonify(resultado)

@app.route('/v1/usuarios/<int:id>/diagnosticos/<int:id_diag>/tratamientos/',methods = ['POST'])
def postTratamiento(id,id_diag):
	id_tratamiento = tratamientos[-1].get('id_tratamiento') + 1
	descripcion = request.json.get('descripcion')
	if not descripcion:
		abort(418)
	frecuencia = request.json.get('frecuencia')
	id_medicamento = request.json.get('id_medicamento')
	if not id_medicamento:
		id_medicamento = 0
	tratamiento = {'id_diag': id_diag,'id_tratamiento':id_tratamiento, 'descripcion': descripcion, 'frecuencia': frecuencia, 'id_medicamento': id_medicamento}
	tratamientos.append(tratamiento)
	return jsonify({'tratamiento':tratamiento}),201

@app.route('/v1/usuarios/<int:id>/diagnosticos/<int:id_diag>/tratamientos/<int:id_tratamiento>/',methods = ['GET'])
def getTratamiento(id,id_diag,id_tratamiento):
    for tratamiento in tratamientos:
        if tratamiento.get('id_diag') == id_diag and tratamiento.get('id_tratamiento') == id_tratamiento:
            return jsonify({'tratamiento':tratamiento})
    abort(404)

@app.route('/v1/usuarios/<int:id>/diagnosticos/<int:id_diag>/tratamientos/<int:id_tratamiento>/',methods = ['PUT'])
def putTratamiento(id,id_diag,id_tratamiento):
	tratamiento = [tratamiento for tratamiento in tratamientos if tratamiento['id_tratamiento'] == id_tratamiento]
	tratamiento[0]['descripcion'] = request.json.get('descripcion', tratamiento[0]['descripcion'])
	if not tratamiento[0]['descripcion']:
		abort(418)
	tratamiento[0]['frecuencia'] = request.json.get('frecuencia', tratamiento[0]['frecuencia'])
	return jsonify({'tratamiento':tratamiento[0]})

@app.route('/v1/usuarios/<int:id>/diagnosticos/<int:id_diag>/tratamientos/<int:id_tratamiento>/',methods = ['DELETE'])
def deleteTratamiento(id,id_diag,id_tratamiento):
	tratamiento = [tratamiento for tratamiento in tratamientos if tratamiento['id_tratamiento'] == id_tratamiento]
	tratamientos.remove(tratamiento[0])
	return jsonify({}), 204 # No content

@app.route('/v1/medicamentos/', methods=['GET'])
def getMedicamentos():
	resultado = []
	for medicamento in medicamentos:
		resultado.append({'medicamento':medicamento})
	return jsonify(resultado)

@app.route('/v1/medicamentos/', methods=['POST'])
def postMedicamentos():
    id_medicamento = medicamentos[-1].get('id_medicamento') + 1
    nombre = request.json.get('nombre')
    if not nombre:
        abort(418)
    medicamento = {'id_medicamento': id_medicamento, 'nombre': nombre}
    medicamentos.append(medicamento)
    return jsonify({'medicamento':medicamento}),201

@app.route('/v1/medicamentos/<int:id_medicamento>/', methods=['GET'])
def getMedicamento(id_medicamento):
    for medicamento in medicamentos:
        if medicamento.get('id_medicamento') == id_medicamento:
            return jsonify({'medicamento':medicamento})
    abort(404)

@app.route('/v1/medicamentos/<int:id_medicamento>/', methods=['PUT'])
def putMedicamento(id_medicamento):
	medicamento = [medicamento for medicamento in medicamentos if medicamento['id_medicamento'] == id_medicamento]
	medicamento[0]['nombre'] = request.json.get('nombre', medicamento[0]['nombre'])
	if not medicamento[0]['nombre']:
		abort(418)
	return jsonify({'medicamento':medicamento[0]})

@app.route('/v1/medicamentos/<int:id_medicamento>/', methods=['DELETE'])
def deleteMedicamento(id_medicamento):
	medicamento = [medicamento for medicamento in medicamentos if medicamento['id_medicamento'] == id_medicamento]
	medicamentos.remove(medicamento[0])
	return jsonify({}), 204 # No content

if __name__ == '__main__':
    app.run()
