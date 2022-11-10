# pip install pipenv
# pipenv install
# pip shell
from flask import Flask
from flask_cors import CORS
from api.cliente_service import cliente
from api.device_service import  device

app = Flask(__name__)
CORS(app,resources={r"/*":{"origins":"*"}})

#
# REGISTRAR AS ROTAS
#
app.register_blueprint(cliente,url_prefix='/api/cliente')
app.register_blueprint(device,url_prefix='/api/device')
#
# OPERAÇÕES
#
@app.route("/")
def info():
    return "API v.1.0"

if __name__ == "__main__":
    app.run(debug=True,host="0.0.0.0")