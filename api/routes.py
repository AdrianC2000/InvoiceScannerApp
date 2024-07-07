import json
import logging

import requests

from flask import Blueprint, Response, request
from flask_restx import Api, Resource, reqparse
from werkzeug.datastructures import FileStorage

from api.routes_handlers import get_invoices_info
from processors.model.invoice_info_response import InvoiceInfoResponse
from settings.json_configurator import JsonConfigurator
from settings.settings import dump_to_json, get_configuration, set_configuration

invoice_blueprint = Blueprint("invoice", __name__)
MIMETYPE = "application/json"

api = Api(invoice_blueprint, version='1.0', title='Invoice Scanner API', description='Backend API',
          url_scheme='/api/invoice_scanner', doc='/doc')
healthcheck_ns = api.namespace('healthcheck', description='Health check')
invoices_ns = api.namespace('invoices', description='Invoices processing')
settings_ns = api.namespace('settings', description='Settings handling')
request_ns = api.namespace('request', description='External API requests handling')

upload_parser = reqparse.RequestParser()
upload_parser.add_argument('file', location='files', type=FileStorage, required=True, action="append")


@healthcheck_ns.route('/', methods=["GET"])
class HealthCheck(Resource):
    @api.response(200, "Success")
    @api.doc(description="Check if application is up")
    def get(self) -> Response:
        return Response(json.dumps({"message": "alive!"}), status=200, mimetype=MIMETYPE)


@invoices_ns.route('/', methods=["POST"])
class Invoices(Resource):
    @api.doc(description="Processing multiple invoices")
    @api.expect(upload_parser)
    @api.response(200, "Success")
    @api.response(206, "Some of the results are not complete due to the input bad format - check messages for details")
    @api.response(415, "One of the files is in the wrong format")
    def post(self) -> Response:
        invoices_files = request.files.getlist("file")
        all_invoices_info = get_invoices_info(invoices_files)
        return self._get_invoices_response(all_invoices_info)

    def _get_invoices_response(self, all_invoices_info: dict[str, InvoiceInfoResponse]) -> Response:
        responses = []
        return_status_code = 200
        for invoice_info_filename, invoice_info in all_invoices_info.items():
            if invoice_info.status != 200:
                return_status_code = 206
            content = self._get_response(invoice_info_filename, invoice_info)
            responses.append(content)
        return Response(dump_to_json(responses), status=return_status_code, mimetype=MIMETYPE)

    @staticmethod
    def _get_response(file_name: str, invoice_info_response: InvoiceInfoResponse) -> dict:
        response_value = invoice_info_response.invoice_info if str(invoice_info_response.status)[0] == '2' else \
            invoice_info_response.message
        return {file_name: response_value}


@settings_ns.route('/', methods=["GET", "POST"])
class Settings(Resource):

    @api.response(200, "Success")
    @api.doc(description="Get actual settings")
    def get(self) -> Response:
        return Response(json.dumps(get_configuration()), status=200, mimetype=MIMETYPE)

    @api.response(200, "Success")
    @api.response(304, "Not modified")
    @api.doc(description="Set new settings")
    def post(self) -> Response:
        if request.get_json() == get_configuration():
            return Response('', status=304)
        set_configuration(dump_to_json(request.get_json()))
        return Response('', status=200)


@settings_ns.route("/customize_json", methods=["POST"])
class SettingsCustomizeJson(Resource):

    @api.response(200, "Success")
    @api.doc(description="Customize extracted invoice information by the current settings.")
    def post(self) -> Response:
        return Response(JsonConfigurator(request.get_json()).customize_json(), status=201, mimetype=MIMETYPE)


@request_ns.route('/', methods=["POST"])
class Request(Resource):

    @api.response(200, "Success")
    @api.doc(description="Send request with your invoice info to endpoint from settings.")
    def post(self) -> Response:
        body = json.dumps(request.get_json(), ensure_ascii=False).encode('utf8').decode()
        logging.info(f"Send request received -> body: {body}")

        url = get_configuration()["url_configuration"]["url"]
        headers = get_configuration()["headers_configuration"]
        body = json.loads(body)

        res = requests.post(url, json=body, headers=headers)
        logging.info(f"Request from {url} -> {res.text}")
        return Response(dump_to_json(res.text), status=201, mimetype=MIMETYPE)
