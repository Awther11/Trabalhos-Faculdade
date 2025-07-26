from flask import Flask, request, jsonify
from flask_cors import CORS

#from config import Config

app = Flask(__name__)
CORS(app)
#app.config.from_object(Config)


# Rota pública: listapromocoes
@app.route('/cadastro', methods=['POST'])
def cadastra():
    data = request.json
    print("===> Dados recebidos")

    campos_obrigatorios = [
        "Nome", "CPF", "Data de Nascimento", "Email",
        "Telefone", "CEP", "Endereço", "Numero da casa",
        "Bairro", "Cidade", "Estado", "Senha", "Confirmar Senha"
    ]

    for campo in campos_obrigatorios:
        if campo not in data or not data[campo].strip():
            return jsonify(f'O campo: {campo} é obrigatório'), 400
        
    if data["Senha"] != data["Confirmar Senha"]:
        return jsonify('As senhas não coincidem'), 400
    

    for campo in campos_obrigatorios:
        print(f"{campo}:", data[campo])

    return jsonify("Dados recebidos com sucesso!"), 200

if __name__ == '__main__':
    app.run(debug=True, port=5055)
