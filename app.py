from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///produtos.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
cors = CORS(app)
db = SQLAlchemy(app) 

class Produto(db.Model):
    id : int = db.Column(db.Integer, primary_key=True)
    nome : str = db.Column(db.String(20), nullable=False)
    descricao : str = db.Column(db.String(200), nullable=False)
    preco : float = db.Column(db.Float, nullable=False)
    codigo : str = db.Column(db.String(10), unique=True, nullable=False)

    def to_json(self):
        return{
            'id':self.id,
            'nome':self.nome,
            'descricao':self.descricao,
            'preco':self.preco,
            'codigo':self.codigo              
        }

@app.route("/", methods=['GET'])
def index():
    produtos = Produto.query.all()
    return jsonify([produto.to_json() for produto in produtos])

@app.route("/<id>", methods=['GET'])
def get(id):
    produto = Produto.query.filter(Produto.id==id).first()
    if produto:
        return jsonify(produto.to_json()), 200
    else:
        return jsonify({'message':'Não foi possivel encontrar o produto.'}), 404

@app.route("/", methods=['POST'])
def create():
    data = request.get_json()
    novoProduto = Produto(
        nome = data['nome'],
        preco = data['preco'],
        descricao = data['descricao'],
        codigo = data['codigo']
    )
    db.session.add(novoProduto)
    db.session.commit()
    return jsonify(novoProduto.to_json()), 201

@app.route("/<id>", methods=['PUT'])
def update(id):
    data = request.get_json()  

    produto = Produto.query.filter(Produto.id==id).first()

    if produto:
        produto.nome=data["nome"] if "nome" in data else produto.nome
        produto.preco=data["preco"] if "preco" in data else produto.preco
        produto.descricao=data["descricao"] if "descricao" in data else produto.descricao
        produto.codigo=data["codigo"] if "codigo" in data else produto.codigo
        db.session.commit()
        return jsonify(produto.to_json()), 202
    else:
        return jsonify({'message':'Não foi possivel encontrar o produto.'}), 404

@app.route("/<id>", methods=['DELETE'])
def delete(id):
    produto = Produto.query.filter(Produto.id==id).first()

    if produto: 
        db.session.delete(produto)
        db.session.commit()
        return jsonify({'message': 'Sucesso ao remover produto.'})
    else:
        return jsonify({'message':'Não foi possivel encontrar o produto.'}), 404

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
