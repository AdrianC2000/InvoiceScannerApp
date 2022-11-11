import json
import logging
import os

import numpy
from PIL import Image
from flask import Blueprint, Response, request

from parsers.json_encoder import JsonEncoder
from processors.invoice_info_processor import InvoiceInfoProcessor
from settings import settings
from settings.settings import customize_json, dump_to_json

invoice_blueprint = Blueprint("invoice", __name__)


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
        img = Image.open(file.stream)
        logging.info(f'File received -> size {img.size}')
        rgb_im = img.convert('RGB')
        invoice_info = InvoiceInfoProcessor(numpy.array(rgb_im), directory).extract_info()
        all_invoices_info.append({file_name: invoice_info})
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
