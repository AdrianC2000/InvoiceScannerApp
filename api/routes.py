import json
import logging
import requests

from flask import Blueprint, Response, request
from api.routes_handlers import get_invoices_info
from settings.settings import customize_json, dump_to_json, get_configuration, set_configuration

invoice_blueprint = Blueprint("invoice", __name__)


@invoice_blueprint.route("/health", methods=["GET"])
def check_health():
    return Response("Alive!", status=200, mimetype='application/json')


@invoice_blueprint.route("/invoice", methods=["POST"])
def process_invoice() -> Response:
    invoices_files = request.files.getlist('image')
    all_invoices_info_json = get_invoices_info(invoices_files)
    return Response(all_invoices_info_json, status=201, mimetype='application/json')


@invoice_blueprint.route("/settings", methods=["GET"])
def get_settings() -> Response:
    return Response(json.dumps(get_configuration()), status=200, mimetype='application/json')


@invoice_blueprint.route("/settings", methods=["POST"])
def set_settings() -> Response:
    if request.get_json() == get_configuration():
        return Response('', status=304)
    else:
        set_configuration(dump_to_json(request.get_json()))
        return Response('', status=200)


@invoice_blueprint.route("/customize_json", methods=["POST"])
def get_customize_json() -> Response:
    return Response(customize_json(request.get_json()), status=201, mimetype='application/json')


@invoice_blueprint.route("/send_request", methods=["POST"])
def send_request() -> Response:
    body = json.dumps(request.get_json(), ensure_ascii=False).encode('utf8').decode()
    logging.info(f"Send request received -> body: {body}")

    url = get_configuration()['url_configuration']['url']
    headers = get_configuration()['headers_configuration']
    body = json.loads(body)

    res = requests.post(url, json=body, headers=headers)
    logging.info(f"Request from {url} -> {res.text}")
    return Response(dump_to_json(res.text), status=201, mimetype='application/json')
