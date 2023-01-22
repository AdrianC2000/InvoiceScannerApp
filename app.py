import logging

from flask import Flask
from flask_cors import CORS
from api.routes import invoice_blueprint

app = Flask(__name__)
CORS(app)
app.register_blueprint(invoice_blueprint)

LOG_FORMAT = "%(asctime)s [%(levelname)s] %(filename)s %(lineno)d - %(message)s"
LOG_FILE = "resources/app.log"
logging.basicConfig(filename=LOG_FILE, filemode='a', format=LOG_FORMAT, encoding='utf-8')
logging.getLogger().setLevel(logging.INFO)

if __name__ == '__main__':
    app.run(debug=True, host="localhost")
    logging.info('App started!')
