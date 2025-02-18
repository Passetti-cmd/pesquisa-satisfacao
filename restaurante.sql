CREATE DATABASE IF NOT EXISTS restaurante_db;
USE restaurante_db;

CREATE TABLE clientes (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(255),
    telefone VARCHAR(20),
    email VARCHAR(255),

    -- Atendimento 👨‍🍳👩‍💼
    tempo_espera_satisfatorio ENUM('Sim', 'Não'),
    atendentes_prestativos ENUM('Sim', 'Não'),

    -- Qualidade da Comida 🍽
    sabor_pratos ENUM('Ruim', 'Regular', 'Bom', 'Ótimo', 'Excelente'),
    variedade_cardapio ENUM('Sim', 'Não'),

    -- Custo-Benefício 💰
    recomendacao ENUM('Ruim', 'Regular', 'Bom', 'Ótimo', 'Excelente'),
    voltaria_pelo_preco ENUM('Sim', 'Não')
);
INSERT INTO clientes (nome, telefone, email, tempo_espera_satisfatorio, atendentes_prestativos, sabor_pratos, variedade_cardapio, recomendacao, voltaria_pelo_preco)
VALUES ('João Silva', '11999999999', 'joao@email.com', 'Sim', 'Sim', 'Ótimo', 'Sim', 'Excelente', 'Sim');
SELECT * FROM clientes;
