import sqlite3

from flask import Blueprint, Flask, jsonify, request

administrator = Blueprint('administrator',__name__)

def conectar():
    return sqlite3.connect('database/data.db')

@administrator.route('/')
def instructions():
    return "Administração"
#
# RETORNAR TODOS OS CLIENTES
#
@administrator.route('/cliente/', methods=['GET'])
def get_all_cliente():
    clientes = []
    try:
        conn = conectar()
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        cur.execute("SELECT * FROM tb_cliente")
        for i in cur.fetchall():
            cliente = {}
            cliente["id"] = i["id"]
            cliente["nome"] = i["nome"]
            cliente["email"] = i["email"]
            cliente["senha"] = i["senha"]
            cliente["telefone1"] = i["telefone1"]
            cliente["telefone2"] = i["telefone2"]
            clientes.append(cliente)
    except Exception as e:
        print(e)
        clientes = []

    return jsonify(clientes)


#
# APAGAR UM CLIENTE
#
@administrator.route('/cliente/<id>', methods=['DELETE'])
def delete_cliente(id):
    print(id)
    try:
        conn = conectar()
        cur = conn.cursor()
        cur.execute("DELETE FROM tb_cliente WHERE id=?",(id,))
        conn.commit()
        resposta = jsonify({'mensagem':'Registro apagado com sucesso'})

    except Exception as e:
        conn.rollback()
        resposta = jsonify({'erro' : str(e)})
    finally:
        conn.close()

    return resposta


#
# RETORNAR TODOS OS DISPOSITIVOS
#
@administrator.route('/device/', methods=['GET'])
def get_all_device():
    devices = []
    try:
        conn = conectar()
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        cur.execute("SELECT * FROM tb_device")

        for i in cur.fetchall():
            device = {}
            device["id"] = int (i["id"])
            device["nome"] = i["nome"]
            device["mac"] = i["mac"]
            device["lock"] = int (i["lock"])
            devices.append(device)
    except Exception as e:
        print(e)
        devices = []

    return jsonify(devices)