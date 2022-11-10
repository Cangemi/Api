import sqlite3

try:
    conn = sqlite3.connect('database/data.db')
    conn.execute('DROP TABLE IF EXISTS tb_cliente')
    conn.execute('DROP TABLE IF EXISTS tb_device')
   
    conn.execute('''
        CREATE TABLE tb_cliente (
            id INTEGER PRIMARY KEY AUTOINCREMENT ,
            nome TEXT NOT NULL,
            email TEXT NOT NULL,
            senha TEXT NOT NULL,
            telefone1 TEXT NOT NULL,
            telefone2 TEXT NOT NULL
        );
    ''')

    conn.execute('''
        CREATE TABLE tb_device (
            id INTEGER PRIMARY KEY AUTOINCREMENT ,
            idCliente INTEGER,
            mac  TEXT NOT NULL,
            nome TEXT NOT NULL,
            lock  INTEGER,
            FOREIGN KEY (idCliente) REFERENCES tb_cliente(id)
        );
        ''')
    
    conn.commit()
    print("Operacao realizada com sucesso!")
    conn.close()
except Exception as e :
    print(e)
