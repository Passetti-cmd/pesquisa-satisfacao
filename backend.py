import os
from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3

app = Flask(__name__)
CORS(app)

# Conecta (ou cria) o banco de dados SQLite restaurante.db
con = sqlite3.connect("restaurante.db", check_same_thread=False)
cursor = con.cursor()

# Cria a tabela se não existir
cursor.execute("""
CREATE TABLE IF NOT EXISTS clientes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT,
    telefone TEXT,
    email TEXT,

    tempo_espera_satisfatorio TEXT,
    atendentes_prestativos TEXT,

    sabor_pratos TEXT,
    variedade_cardapio TEXT,

    recomendacao TEXT,
    voltaria_pelo_preco TEXT
)
""")
con.commit()

@app.route("/")
def home():
    return jsonify({"mensagem": "API do Restaurante está funcionando com SQLite!"})

# Rota para receber dados do formulário
@app.route("/salvar", methods=["POST"])
def salvar_dados():
    try:
        dados = request.json
        cursor.execute("""
            INSERT INTO clientes (
                nome, telefone, email,
                tempo_espera_satisfatorio, atendentes_prestativos,
                sabor_pratos, variedade_cardapio,
                recomendacao, voltaria_pelo_preco
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
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
        con.commit()
        return jsonify({"mensagem": "Dados salvos com sucesso!"}), 201

    except Exception as e:
        return jsonify({"erro": str(e)}), 500

# Rota para listar feedbacks
@app.route("/feedbacks", methods=["GET"])
def listar_feedbacks():
    cursor.execute("SELECT * FROM clientes ORDER BY id DESC")
    colunas = [desc[0] for desc in cursor.description]
    dados = [dict(zip(colunas, row)) for row in cursor.fetchall()]
    return jsonify(dados)

if __name__ == "__main__":
    # Lê a porta a partir de variável de ambiente (Render/Heroku), senão usa 5000
    port = int(os.environ.get("PORT", 5000))
    # Faz o bind no host 0.0.0.0 para o Render detectar a porta aberta
    app.run(host="0.0.0.0", port=port, debug=True)
