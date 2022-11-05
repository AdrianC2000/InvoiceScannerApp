import logging

from flask import Flask

from api.routes import invoice_blueprint

UPLOAD_FOLDER = 'resources/upload'
ALLOWED_EXTENSIONS = set(['pdf', 'png', 'jpg', 'jpeg'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.register_blueprint(invoice_blueprint)

LOG_FORMAT = "%(asctime)s [%(levelname)s] %(filename)s %(lineno)d - %(message)s"
logging.basicConfig(filename='resources/app.log', filemode='a', format=LOG_FORMAT, encoding='utf-8')
logging.getLogger().setLevel(logging.INFO)

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")
    logging.info('App started!')
