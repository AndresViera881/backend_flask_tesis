from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root@localhost/bdclientes'

db = SQLAlchemy(app)
ma = Marshmallow(app)


class tbl_clientes(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ape = db.Column(db.String)
    nom = db.Column(db.String)
    email = db.Column(db.String)

    def __init__(self, ape, nom, email):
        self.ape = ape
        self.nom = nom
        self.email = email


class ClientesSchema(ma.Schema):
    class Meta:
        fields = ('ape', 'nom', 'email')


# Este objeto me permitira serializar todos los clientes de mi tabla
clientes_schema = ClientesSchema(many=True)
# Este objeto me permitira serializar un cliente de mi tabla
cli_schema = ClientesSchema()


# EndPoint GET todos los clientes
@app.route('/clientes', methods=['GET'])
def clientes():
    # Esto como el select * from tbl_clientes
    clientes = tbl_clientes.query.all()
    result = clientes_schema.dump(clientes)
    return jsonify(result)


# EndPoint GET find id un solo cliente
@app.route('/cliente/<id>', methods=['GET'])
def cliente(id):
    # Esto como el select * from tbl_clientes
    cliente = tbl_clientes.query.get(id)
    return cli_schema.jsonify(cliente)


# EndPoint POST add cliente
@app.route('/cliente', methods=['POST'])
def add_cliente():
    # Esto para insertar datos
    ape = request.json['ape']
    nom = request.json['nom']
    email = request.json['email']
    new_cliente = tbl_clientes(ape, nom, email)
    db.session.add(new_cliente)
    db.session.commit()
    cliente = tbl_clientes.query.get(new_cliente.id)
    # Aqui enviamos el esquema que es para un solo registro, utilizamos el mismo esquema que el find
    return cli_schema.jsonify(cliente)


# EndPoint UPDATE cliente
@app.route('/cliente/<id>', methods=['PUT'])
def update_cliente(id):
    # Esto para modificar datos
    cliente = tbl_clientes.query.get(id)
    # Los datos que mandara el fron-end en formato json
    ape = request.json['ape']
    nom = request.json['nom']
    email = request.json['email']
    # Actualizamos la informacion en el objeto y luego actualizo la tabla
    cliente.ape = ape
    cliente.nom = nom
    cliente.email = email
    db.session.commit()
    # Aqui enviamos el esquema que es para un solo registro, utilizamos el mismo esquema que el find
    return cli_schema.jsonify(cliente)


# EndPoint DELETE cliente
@app.route('/cliente/<id>', methods=['DELETE'])
def delete_cliente(id):
    # Buscamos al cliente
    cliente = tbl_clientes.query.get(id)
    db.session.delete(cliente)
    db.session.commit()
    return cli_schema.jsonify(cliente)


app.run(debug=True)
