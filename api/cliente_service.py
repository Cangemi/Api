import sqlite3

from flask import Blueprint, Flask, jsonify, request

cliente = Blueprint('cliente',__name__)

def conectar():
    return sqlite3.connect('database/data.db')

@cliente.route('/')
def instructions():
    return "Clientes"
#
# RETORNAR CLIENTE PELO ID
#
@cliente.route('/<id>', methods=['GET'])
def get_by_id(id):
    cliente = {}
    try:
        conn = conectar()
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        cur.execute("SELECT * FROM tb_cliente where id=?",(id,))
        row = cur.fetchone()
       
        cliente["id"] = row["id"]
        cliente["nome"] = row["nome"]
        cliente["email"] = row["email"]
        cliente["senha"] = row["senha"]
        cliente["telefone1"] = row["telefone1"]
        cliente["telefone2"] = row["telefone2"]
           
    except Exception as e:
        print(str(e))
        cliente = {}

    return jsonify(cliente)

#
# RETORNAR CLIENTE Por EMAIL E SENHA
#
@cliente.route('/<email>/<senha>', methods=['GET'])
def get_by_email(email,senha):
    cliente = {}
    try:
        conn = conectar()
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        cur.execute("SELECT * FROM tb_cliente where email=? and  senha=?",(email,senha))
        row = cur.fetchone()
       
        cliente["id"] = row["id"]
        cliente["nome"] = row["nome"]
        cliente["email"] = row["email"]
        cliente["senha"] = row["senha"]
        cliente["telefone1"] = row["telefone1"]
        cliente["telefone2"] = row["telefone2"]
           
    except Exception as e:
        print(str(e))
        cliente = {}

    return jsonify(cliente)


#
# ADICIONAR UM NOVO CLIENTE
#
@cliente.route('/', methods=['POST'])
def add():
    cliente = request.get_json()
    try:
        conn = conectar()
        cur = conn.cursor()
        cur.execute("INSERT INTO tb_cliente (nome, email,senha, telefone1, telefone2) VALUES (?, ?, ?, ?, ?)",
                    (cliente['nome'], cliente['email'], cliente['senha'], cliente['telefone1'],cliente['telefone2']) )
        conn.commit()
        resposta = jsonify(
            {
                'mensagem':'Operacao realizada com sucesso',
                'id' : cur.lastrowid
            }
        )
    except Exception as e:
        conn.rollback()
        resposta = jsonify({'erro' : str(e)})
    finally:
        conn.close()
    return resposta

#
# ATUALIZAR UM CLIENTE
#
@cliente.route('/', methods=['PUT'])
def update():
    cliente = request.get_json()

    try:
        conn = conectar()
        cur = conn.cursor()
        cur.execute("UPDATE tb_cliente SET nome=?, email=?,senha=?, telefone1=?, telefone2=? WHERE id=?",
                    (cliente['nome'], cliente['email'], cliente['senha'], cliente['telefone1'],cliente['telefone2'], cliente['id']) )
        conn.commit()
        resposta = jsonify({'mensagem':'Operacao realizada com sucesso'})

    except Exception as e:
        conn.rollback()
        resposta = jsonify({'erro' : str(e)})
    finally:
        conn.close()

    return resposta