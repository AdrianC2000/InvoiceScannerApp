import json

from invoice_processing_utils.parsers.json_encoder import JsonEncoder


def get_configuration() -> json:
    with open('settings/configuration.json', mode="r", encoding="utf-8") as f:
        return json.load(f)


def set_configuration(settings_json: json):
    with open('settings/configuration.json', 'w') as settings_file:
        settings_file.write(settings_json)


def dump_to_json(obj) -> json:
    return json.dumps(obj, indent=4, cls=JsonEncoder, ensure_ascii=False)
