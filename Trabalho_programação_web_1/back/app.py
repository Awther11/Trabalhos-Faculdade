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

    # Validação de campos obrigatórios
    for campo in campos_obrigatorios:
        # Usamos `data.get(campo)` para evitar KeyError se o campo não estiver presente
        # E verificamos se o valor existe e não é uma string vazia após strip()
        if not data.get(campo) or not str(data.get(campo)).strip():
            return jsonify({"mensagem": f'O campo "{campo}" é obrigatório.'}), 400
        
    # Validação de senhas
    if data["Senha"] != data["Confirmar Senha"]:
        return jsonify({"mensagem": 'As senhas não coincidem.'}), 400
    
    # Validações de formato e unicidade
    
    # Validação de E-mail
    email = data["Email"].strip()
    if not email or '@' not in email or '.' not in email:
        return jsonify({"mensagem": "Formato de e-mail inválido."}), 400
    if Cad_Usuario.query.filter_by(email=email).first():
        return jsonify({"mensagem": "E-mail já cadastrado."}), 409

    # Validação de CPF
    cpf = data["CPF"].strip()
    if not cpf.isdigit() or len(cpf) != 11:
        return jsonify({"mensagem": "CPF inválido. Deve conter 11 dígitos numéricos."}), 400
    if Cad_Usuario.query.filter_by(cpf=cpf).first():
        return jsonify({"mensagem": "CPF já cadastrado."}), 409

    # Validação de Telefone
    telefone = data["Telefone"].strip()
    # Exemplo: remover caracteres não numéricos se o frontend permitir, ou exigir só números
    telefone_numeros = ''.join(filter(str.isdigit, telefone))
    if not telefone_numeros or len(telefone_numeros) < 10: # Ajuste o tamanho mínimo conforme necessário
         return jsonify({"mensagem": "Telefone inválido. Deve conter apenas dígitos numéricos e um tamanho válido."}), 400
    if Cad_Usuario.query.filter_by(telefone=telefone_numeros).first():
        return jsonify({"mensagem": "Telefone já cadastrado."}), 409

    # Validação de Data de Nascimento
    try:
        data_nascimento_obj = date.fromisoformat(data["Data de Nascimento"].strip()) # Espera formato YYYY-MM-DD
    except ValueError:
        return jsonify({"mensagem": "Formato de Data de Nascimento inválido. Use YYYY-MM-DD."}), 400

    # Validação de Nickname (se fornecido)
    nickname = data.get("Nickname", "").strip()
    if nickname and Cad_Usuario.query.filter_by(nickname=nickname).first():
        return jsonify({"mensagem": "Nickname já cadastrado."}), 409

    # --- Criação e salvamento no Banco de Dados ---
    try:
        novo_usuario = Cad_Usuario(
            nome=data["Nome"].strip(),
            nickname=nickname if nickname else None, # Salva None se vazio
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
        novo_usuario.set_senha(data["Senha"]) # Hash da senha

        db.session.add(novo_usuario)
        db.session.commit()

        # Retorna os dados do usuário recém-criado (sem a senha hash)
        return jsonify({"mensagem": "Usuário cadastrado com sucesso!", "usuario": novo_usuario.to_dict()}), 201

    except Exception as e:
        db.session.rollback() # Em caso de erro, desfaz a transação
        print(f"Erro ao cadastrar usuário: {e}")
        return jsonify({"mensagem": "Erro interno ao cadastrar usuário. Tente novamente mais tarde."}), 500

@app.route('/login', methods=['POST'])
def fazer_login():
    dados = request.get_json()
    identificador = dados.get('identificador') # Pode ser email ou CPF
    senha = dados.get('senha')

    if not identificador or not senha:
        return jsonify({"mensagem": "Identificador (e-mail ou CPF) e senha são obrigatórios"}), 400

    usuario = None
    # Tenta encontrar o usuário por e-mail
    if '@' in identificador:
        usuario = Cad_Usuario.query.filter_by(email=identificador).first()
    # Se não for e-mail ou não encontrado, tenta por CPF
    if not usuario and identificador.isdigit() and len(identificador) == 11:
        usuario = Cad_Usuario.query.filter_by(cpf=identificador).first()

    if usuario and usuario.verificar_senha(senha):
        token_acesso = create_access_token(identity=usuario.id)
        return jsonify(token_acesso=token_acesso, usuario=usuario.to_dict()), 200
    else:
        return jsonify({"mensagem": "Credenciais inválidas"}), 401

@app.route('/perfil', methods=['GET'])
@jwt_required()
def obter_perfil():
    # Obtém o ID do usuário a partir do token JWT
    id_usuario_atual = get_jwt_identity()
    usuario = Cad_Usuario.query.get(id_usuario_atual)

    if not usuario:
        return jsonify({"mensagem": "Usuário não encontrado."}), 404
    
    return jsonify(usuario.to_dict()), 200

# --- Inicialização do Aplicativo ---
if __name__ == '__main__':
    with app.app_context():
        # Cria as tabelas do banco de dados se elas não existirem
        db.create_all()
    app.run(debug=True) # `debug=True` habilita o modo de depuração (recarga automática, etc.)