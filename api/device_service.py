from flask import Flask, Blueprint, request, jsonify
import sqlite3

device = Blueprint('device',__name__)

def conectar():
    return sqlite3.connect('database/data.db')


@device.route('/')
def instructions():
    return "Dispositivo"

#region DEVICE PELO ID

@device.route('/<id>', methods=['GET'])
def get_by_id(id):
    devices = []
    device = {}
    try:
        conn = conectar()
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        cur.execute("SELECT tb_device.*,tb_cliente.id as idCliente FROM tb_device INNER JOIN tb_cliente on tb_cliente.id = tb_device.idCliente where tb_device.idCliente=?",(id,))
        
       
        for i in cur.fetchall():
            device = {}
            device["id"] = int (i["id"])
            device["nome"] = i["nome"]
            device["mac"] = i["mac"]
            device["lock"] =  i["lock"]
            device["idCliente"] = i["idCliente"]
            devices.append(device)
           
    except Exception as e:
        print(str(e))
        devices = []

    return jsonify(devices)

#PESQUISAR DISPOSITIVO POR MAC

@device.route('/address/<mac>', methods=['GET'])
def get_by_mac(mac):
    device = {}
    try:
        conn = conectar()
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        cur.execute("SELECT * FROM tb_device where mac=?",(mac,))
        row = cur.fetchone()
       
        device["id"] = row["id"]
        device["nome"] = row["nome"]
        device["mac"] = row["mac"]
        device["lock"] =  row["lock"]
           
    except Exception as e:
        print(str(e))
        device = {}

    return jsonify(device)

#endregion

#
# ADICIONAR UM NOVO DISPOSITIVO
#
@device.route('/', methods=['POST'])
def add():
    device = request.get_json()
    try:
        conn = conectar()
        cur = conn.cursor()
        cur.execute("INSERT INTO tb_device (nome, mac, lock, idCliente) VALUES (?, ?, ?, ?)",
                    (device['nome'], device['mac'],device['lock'], device['idCliente']) )
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
# ATUALIZAR UM DISPOSITIVO
#
@device.route('/', methods=['PUT'])
def update():
    device = request.get_json()

    try:
        conn = conectar()
        cur = conn.cursor()
        cur.execute("UPDATE tb_device SET nome=?, mac=?, lock=? WHERE id=?",
                    (device['nome'],device['mac'],device['lock'], device['id']))
        conn.commit()
        resposta = jsonify({'mensagem':'Operacao realizada com sucesso'})

    except Exception as e:
        conn.rollback()
        resposta = jsonify({'erro' : str(e)})
    finally:
        conn.close()

    return resposta





#
# APAGAR UM DISPOSITIVO
#
@device.route('/<id>', methods=['DELETE'])
def delete(id):
    print(id)
    try:
        conn = conectar()
        cur = conn.cursor()
        cur.execute("DELETE FROM tb_device WHERE id=?",(id,))
        conn.commit()
        resposta = jsonify({'mensagem':'Registro apagado com sucesso'})

    except Exception as e:
        conn.rollback()
        resposta = jsonify({'erro' : str(e)})
    finally:
        conn.close()

    return resposta