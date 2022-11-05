import base64
import json
import logging

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
    file = request.files['image']
    img = Image.open(file.stream)
    logging.info(f'File received -> size {img.size}')
    rgb_im = img.convert('RGB')
    rgb_im.save("resources/upload/image.jpg")
    invoice_info = InvoiceInfoProcessor(numpy.array(rgb_im)).extract_info()
    return Response(json.dumps(invoice_info, indent=4, cls=JsonEncoder, ensure_ascii=False),
                    status=201, mimetype='application/json')
