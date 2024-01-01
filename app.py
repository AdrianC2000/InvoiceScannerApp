import logging

from flask import Flask
from flask_cors import CORS
from api.routes import invoice_blueprint

app = Flask(__name__)
CORS(app)
app.register_blueprint(invoice_blueprint)


def configure_logging():
    log_format = "%(asctime)s [%(levelname)s] %(filename)s %(lineno)d - %(message)s"
    log_file = "resources/app.log"

    formatter = logging.Formatter(log_format)

    file_handler = logging.FileHandler(log_file, mode='a', encoding='utf-8')
    file_handler.setFormatter(formatter)

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)

    root_logger = logging.getLogger()
    root_logger.addHandler(file_handler)
    root_logger.addHandler(console_handler)

    root_logger.setLevel(logging.INFO)


def list_routes():
    result = ""
    for rule in app.url_map.iter_rules():
        methods = ', '.join(rule.methods)
        result += f"Endpoint: {rule.endpoint}, Methods: {methods}, Path: {rule}\n"
    return result


if __name__ == '__main__':
    configure_logging()

    with app.app_context():
        logging.info(f'Available routes: \n{list_routes()}')
        logging.info(f'App started!')

    app.run(debug=True, host="localhost", use_reloader=False)
