from flask import Flask, request, jsonify
import mysql.connector
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Permite que o frontend (HTML em outro lugar) faça requisições sem erro de CORS

# Conectar ao banco de dados MySQL
db = mysql.connector.connect(
    host="localhost",  # Ou "127.0.0.1"
    user="root",       # Seu usuário do MySQL
    password="Yutah137#",  # Sua senha do MySQL
    database="restaurante_db"  # Nome do banco de dados
)

cursor = db.cursor()

# Criar a tabela se não existir
cursor.execute("""
CREATE TABLE IF NOT EXISTS clientes (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(255),
    telefone VARCHAR(20),
    email VARCHAR(255),
    tempo_espera_satisfatorio ENUM('Sim', 'Não'),
    atendentes_prestativos ENUM('Sim', 'Não'),
    sabor_pratos ENUM('Ruim', 'Regular', 'Bom', 'Ótimo', 'Excelente'),
    variedade_cardapio ENUM('Sim', 'Não'),
    recomendacao ENUM('Ruim', 'Regular', 'Bom', 'Ótimo', 'Excelente'),
    voltaria_pelo_preco ENUM('Sim', 'Não')
)
""")
db.commit()

@app.route("/")
def home():
    return jsonify({"mensagem": "API do Restaurante está funcionando!"})

# Rota para receber os dados do formulário
@app.route("/salvar", methods=["POST"])
def salvar_dados():
    try:
        dados = request.json
        cursor.execute("""
            INSERT INTO clientes
            (nome, telefone, email,
             tempo_espera_satisfatorio, atendentes_prestativos,
             sabor_pratos, variedade_cardapio,
             recomendacao, voltaria_pelo_preco)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (
            dados["nome"],
            dados["telefone"],
            dados["email"],
            dados["tempo_espera_satisfatorio"],
            dados["atendentes_prestativos"],
            dados["sabor_pratos"],
            dados["variedade_cardapio"],
            dados["recomendacao"],
            dados["voltaria_pelo_preco"]
        ))
        db.commit()
        return jsonify({"mensagem": "Dados salvos com sucesso!"}), 201

        
    
    except Exception as e:
        return jsonify({"erro": str(e)}), 500


@app.route("/feedbacks", methods=["GET"])
def listar_feedbacks():
    cursor.execute("SELECT * FROM clientes ORDER BY id DESC")
    colunas = [desc[0] for desc in cursor.description]  # Obtém os nomes das colunas
    dados = [dict(zip(colunas, row)) for row in cursor.fetchall()]
    return jsonify(dados)

if __name__ == "__main__":
    app.run(debug=True)
