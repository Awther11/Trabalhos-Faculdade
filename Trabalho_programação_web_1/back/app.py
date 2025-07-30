import os
from datetime import timedelta, date # Importe date para lidar com datas

from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import create_access_token, jwt_required, JWTManager, get_jwt_identity
from werkzeug.security import generate_password_hash, check_password_hash
from flask_cors import CORS

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(os.path.abspath(os.getcwd()), 'usuarios.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False 
db = SQLAlchemy(app)

app.config['JWT_SECRET_KEY'] = 'VcKzHS4g2h+dP33tCbqOghtKaU37wvFECMhVqrfccaoI/17qh/j3+VDV'
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(minutes=3)
jwt = JWTManager(app)

CORS(app)

class Cad_Usuario(db.Model):
    __tablename__ = 'cad_usuarios' 
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    nickname = db.Column(db.String(50), unique=True, nullable=True)
    cpf = db.Column(db.String(11), unique=True, nullable=False)
    data_nascimento = db.Column(db.Date, unique=False, nullable=False) 
    email = db.Column(db.String(120), unique=True, nullable=False)
    telefone = db.Column(db.String(13), unique=True, nullable=False)
    cep = db.Column(db.String(8), unique=False, nullable=False)
    endereco = db.Column(db.String(100), unique=False, nullable=False)
    numero = db.Column(db.String(5), unique=False, nullable=False)
    complemento = db.Column(db.String(100), unique=False, nullable=True)
    bairro = db.Column(db.String(100), unique=False, nullable=False)
    cidade = db.Column(db.String(100), unique=False, nullable=False)
    estado = db.Column(db.String(100), unique=False, nullable=False)
    plataforma_favorita = db.Column(db.String(100), unique=False, nullable=True)
    genero_jogo_favorito = db.Column(db.String(100), unique=False, nullable=True)
    senha_hash = db.Column(db.String(128), nullable=False)
    
    def set_senha(self, senha):
        self.senha_hash = generate_password_hash(senha)

    def verificar_senha(self, senha):
        return check_password_hash(self.senha_hash, senha)

    def to_dict(self):
        return {
            "id": self.id,
            "nome": self.nome,
            "nickname": self.nickname,
            "cpf": self.cpf,
            "data_nascimento": self.data_nascimento,
            "email": self.email,
            "telefone": self.telefone,
            "cep": self.cep,
            "endereco": self.endereco,
            "numero": self.numero,
            "complemento": self.complemento,
            "bairro": self.bairro,
            "cidade": self.cidade,
            "estado": self.estado,
            "plataforma_favorita": self.plataforma_favorita,
            "genero_jogo_favorito": self.genero_jogo_favorito
        }



@app.route('/cadastro', methods=['POST'])
def cadastra():
    data = request.json
    print("===> Dados recebidos para cadastro:")
    
    campos_obrigatorios = [
        "Nome", "CPF", "Data de Nascimento", "Email",
        "Telefone", "CEP", "Endereço", "Numero da casa",
        "Bairro", "Cidade", "Estado", "Senha", "Confirmar Senha"
    ]


    for campo in campos_obrigatorios:
        if not data.get(campo) or not str(data.get(campo)).strip():
            return jsonify({"mensagem": f'O campo "{campo}" é obrigatório.'}), 400
        

    if data["Senha"] != data["Confirmar Senha"]:
        return jsonify({"mensagem": 'As senhas não coincidem.'}), 400
    

    

    email = data["Email"].strip()
    if not email or '@' not in email or '.' not in email:
        return jsonify({"mensagem": "Formato de e-mail inválido."}), 400
    if Cad_Usuario.query.filter_by(email=email).first():
        return jsonify({"mensagem": "E-mail já cadastrado."}), 409


    cpf = data["CPF"].strip()
    if not cpf.isdigit() or len(cpf) != 11:
        return jsonify({"mensagem": "CPF inválido. Deve conter 11 dígitos numéricos."}), 400
    if Cad_Usuario.query.filter_by(cpf=cpf).first():
        return jsonify({"mensagem": "CPF já cadastrado."}), 409

    
    telefone = data["Telefone"].strip()
 
    telefone_numeros = ''.join(filter(str.isdigit, telefone))
    if not telefone_numeros or len(telefone_numeros) < 10: 
         return jsonify({"mensagem": "Telefone inválido. Deve conter apenas dígitos numéricos e um tamanho válido."}), 400
    if Cad_Usuario.query.filter_by(telefone=telefone_numeros).first():
        return jsonify({"mensagem": "Telefone já cadastrado."}), 409


    try:
        data_nascimento_obj = date.fromisoformat(data["Data de Nascimento"].strip()) 
    except ValueError:
        return jsonify({"mensagem": "Formato de Data de Nascimento inválido. Use YYYY-MM-DD."}), 400


    nickname = data.get("Nickname", "").strip()
    if nickname and Cad_Usuario.query.filter_by(nickname=nickname).first():
        return jsonify({"mensagem": "Nickname já cadastrado."}), 409


    try:
        novo_usuario = Cad_Usuario(
            nome=data["Nome"].strip(),
            nickname=nickname if nickname else None, 
            cpf=cpf,
            data_nascimento=data_nascimento_obj,
            email=email,
            telefone=telefone_numeros,
            cep=data["CEP"].strip(),
            endereco=data["Endereço"].strip(),
            numero=data["Numero da casa"].strip(),
            complemento=data.get("Complemento", "").strip() if data.get("Complemento") else None,
            bairro=data["Bairro"].strip(),
            cidade=data["Cidade"].strip(),
            estado=data["Estado"].strip(),
            plataforma_favorita=data.get("Plataforma Favorita", "").strip() if data.get("Plataforma Favorita") else None,
            genero_jogo_favorito=data.get("Genero de Jogo Favorito", "").strip() if data.get("Genero de Jogo Favorito") else None
        )
        novo_usuario.set_senha(data["Senha"]) 

        db.session.add(novo_usuario)
        db.session.commit()

 
        return jsonify({"mensagem": "Usuário cadastrado com sucesso!", "usuario": novo_usuario.to_dict()}), 201

    except Exception as e:
        db.session.rollback() 
        print(f"Erro ao cadastrar usuário: {e}")
        return jsonify({"mensagem": "Erro interno ao cadastrar usuário. Tente novamente mais tarde."}), 500

# @app.route('/login', methods=['POST'])
# def fazer_login():
#     dados = request.get_json()
#     identificador = dados.get('identificador') # Pode ser email ou CPF
#     senha = dados.get('senha')

#     if not identificador or not senha:
#         return jsonify({"mensagem": "Identificador (e-mail ou CPF) e senha são obrigatórios"}), 400

#     usuario = None
   
#     if '@' in identificador:
#         usuario = Cad_Usuario.query.filter_by(email=identificador).first()
    
#     if not usuario and identificador.isdigit() and len(identificador) == 11:
#         usuario = Cad_Usuario.query.filter_by(cpf=identificador).first()

#     if usuario and usuario.verificar_senha(senha):
#         token_acesso = create_access_token(identity=usuario.id)
#         return jsonify(token_acesso=token_acesso, usuario=usuario.to_dict()), 200
#     else:
#         return jsonify({"mensagem": "Credenciais inválidas"}), 401



@app.route('/login', methods=['POST'])
def fazer_login():
    dados = request.get_json()
    if not dados:
        return jsonify({"mensagem": "Nenhum dado enviado"}), 400

    identificador = dados.get('identificador')
    senha = dados.get('senha')

    if not identificador or not senha:
        return jsonify({"mensagem": "Identificador (e-mail ou CPF) e senha são obrigatórios"}), 400

    usuario = None

    # Verifica se o identificador parece ser um email
    if '@' in identificador:
        usuario = Cad_Usuario.query.filter_by(email=identificador.strip()).first()

    # Se não encontrado, tenta pelo CPF (número com 11 dígitos)
    if not usuario and identificador.isdigit() and len(identificador) == 11:
        usuario = Cad_Usuario.query.filter_by(cpf=identificador.strip()).first()

    # Se usuário encontrado, verifica a senha
    if usuario and usuario.verificar_senha(senha):
        token_acesso = create_access_token(identity=usuario.id)
        return jsonify(token_acesso=token_acesso, usuario=usuario.to_dict()), 200
    else:
        return jsonify({"mensagem": "Credenciais inválidas"}), 401



# @app.route('/login', methods=['POST'])
# def fazer_login():
#     dados = request.get_json()
#     identificador = dados.get('identificador')  # email ou CPF
#     senha = dados.get('senha')

#     if not identificador or not senha:
#         return jsonify({"mensagem": "Identificador e senha são obrigatórios"}), 400

#     usuario = None

#     if '@' in identificador:
#         usuario = Cad_Usuario.query.filter_by(email=identificador).first()
#     elif identificador.isdigit() and len(identificador) == 11:
#         usuario = Cad_Usuario.query.filter_by(cpf=identificador).first()

#     if usuario and usuario.verificar_senha(senha):
#         token = create_access_token(identity=usuario.id)
#         return jsonify({
#             "token_acesso": token,
#             "usuario": usuario.to_dict()
#         }), 200
#     else:
#         return jsonify({"mensagem": "Credenciais inválidas"}), 401


class Produto(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    descricao = db.Column(db.String(500), nullable=True)
    preco = db.Column(db.Float, nullable=False)
    imagem_url = db.Column(db.String(255), nullable=False)
    estoque = db.Column(db.Integer, default=0)

    def to_dict(self):
        return {
            "id": self.id,
            "nome": self.nome,
            "descricao": self.descricao,
            "preco": self.preco,
            "imagem_url": self.imagem_url,
            "estoque": self.estoque
        }


@app.route('/produto', methods=['POST'])
def cadastrar_produto():
    data = request.json

    campos_obrigatorios = ["nome", "preco", "imagem_url"]

    for campo in campos_obrigatorios:
        if not data.get(campo):
            return jsonify({"mensagem": f"O campo '{campo}' é obrigatório."}), 400

    try:
        produto = Produto(
            nome=data["nome"].strip(),
            descricao=data.get("descricao", "").strip(),
            preco=float(data["preco"]),
            imagem_url=data["imagem_url"].strip(),
            estoque=int(data.get("estoque", 0))
        )

        db.session.add(produto)
        db.session.commit()

        return jsonify({"mensagem": "Produto cadastrado com sucesso!", "produto": produto.to_dict()}), 201

    except Exception as e:
        db.session.rollback()
        print(f"Erro ao cadastrar produto: {e}")
        return jsonify({"mensagem": "Erro interno ao cadastrar produto."}), 500





class Categoria(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False, unique=True)
    descricao = db.Column(db.String(255), nullable=True)

    def to_dict(self):
        return {
            "id": self.id,
            "nome": self.nome,
            "descricao": self.descricao
        }
@app.route('/categoria', methods=['POST'])
def cadastrar_categoria():
    data = request.json

    if not data.get('nome'):
        return jsonify({"mensagem": "O campo 'nome' é obrigatório."}), 400

    nome = data['nome'].strip()
    descricao = data.get('descricao', '').strip()

    if Categoria.query.filter_by(nome=nome).first():
        return jsonify({"mensagem": "Essa categoria já existe."}), 409

    try:
        nova_categoria = Categoria(nome=nome, descricao=descricao)
        db.session.add(nova_categoria)
        db.session.commit()

        return jsonify({"mensagem": "Categoria cadastrada com sucesso!", "categoria": nova_categoria.to_dict()}), 201

    except Exception as e:
        db.session.rollback()
        print(f"Erro ao cadastrar categoria: {e}")
        return jsonify({"mensagem": "Erro interno ao cadastrar categoria."}), 500
    


@app.route('/categoria/<int:id>', methods=['GET'])
def obter_categoria(id):
    categoria = Categoria.query.get(id)

    if not categoria:
        return jsonify({"mensagem": "Categoria não encontrada."}), 404

    return jsonify(categoria.to_dict()), 200



@app.route('/produto/<int:id>', methods=['GET'])
def obter_detalhes_produto(id):
    produto = Produto.query.get(id)

    if not produto:
        return jsonify({"mensagem": "Produto não encontrado."}), 404

    return jsonify(produto.to_dict()), 200




if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)