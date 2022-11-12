# pip install pipenv
# pipenv install
# pip shell
from flask import Flask
from flask_cors import CORS

from api.cliente_service import cliente
from api.device_service import device
from api.administrator_service import administrator

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})


#
# REGISTRAR AS ROTAS
#
app.register_blueprint(cliente,url_prefix='/api/cliente')
app.register_blueprint(device,url_prefix='/api/device')
app.register_blueprint(administrator,url_prefix='/api/admin')

@app.route('/')
def instructions():
    return "API"

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)