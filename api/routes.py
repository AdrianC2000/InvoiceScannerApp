import json
import logging
import os
import requests

from flask import Blueprint, Response, request
from entities.invoice_info_response import InvoiceInfoResponse
from invoice_processing_utils.format_unifier import FormatUnifier
from processors.invoice_info_processor import InvoiceInfoProcessor
from settings import settings
from settings.settings import customize_json, dump_to_json

invoice_blueprint = Blueprint("invoice", __name__)


def get_response(file_name: str, invoice_info_response: InvoiceInfoResponse) -> dict:
    if str(invoice_info_response.status)[0] == '2':
        response_value = invoice_info_response.invoice_info
    else:
        response_value = invoice_info_response.message
    return {file_name: response_value}


@invoice_blueprint.route("/health", methods=["GET"])
def check_health():
    return Response("Alive!", status=200, mimetype='application/json')


@invoice_blueprint.route("/invoice", methods=["POST"])
def process_invoice():
    files = request.files.getlist('image')
    all_invoices_info = list()
    cwd = os.getcwd()
    for file in files:
        directory = cwd + '/resources/entire_flow/' + file.filename + "/"
        if not os.path.exists(directory):
            os.makedirs(directory)
        file_name = file.filename
        invoice = FormatUnifier(directory, file).unify_format()
        invoice_info_response = InvoiceInfoProcessor(invoice, directory).extract_info()
        content = get_response(file_name, invoice_info_response)
        all_invoices_info.append(content)
    all_invoices_info_json = dump_to_json(all_invoices_info)
    return Response(all_invoices_info_json, status=201, mimetype='application/json')


@invoice_blueprint.route("/settings", methods=["GET"])
def get_settings():
    return Response(json.dumps(settings.get_configuration()), status=200, mimetype='application/json')


@invoice_blueprint.route("/settings", methods=["POST"])
def set_settings():
    if request.get_json() == settings.get_configuration():
        return Response('', status=304)
    else:
        settings.set_configuration(dump_to_json(request.get_json()))
        return Response('', status=200)


@invoice_blueprint.route("/customize_json", methods=["POST"])
def get_customize_json():
    return Response(customize_json(request.get_json()), status=201, mimetype='application/json')


@invoice_blueprint.route("/send_request", methods=["POST"])
def send_request():
    body = json.dumps(request.get_json(), ensure_ascii=False).encode('utf8').decode()
    logging.info(f"Send request received -> body: {body}")
    url = settings.get_configuration()['url_configuration']['url']
    headers = settings.get_configuration()['headers_configuration']
    body = json.loads(body)
    res = requests.post(url, json=body, headers=headers)
    logging.info(f"Request from {url} ->" + res.text)
    return Response(dump_to_json(res.text), status=201, mimetype='application/json')
