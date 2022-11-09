import base64
import json
import logging
import os

import cv2
import numpy
import numpy as np
from PIL import Image
from flask import Blueprint, Response, request, jsonify

from parsers.json_encoder import JsonEncoder
from processors.invoice_info_processor import InvoiceInfoProcessor

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
    return Response(json.dumps(all_invoices_info, indent=4, cls=JsonEncoder, ensure_ascii=False),
                    status=201, mimetype='application/json')
