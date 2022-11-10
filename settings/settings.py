import json
from settings.configuration import SETTINGS


def get_configuration() -> json:
    return json.dumps(SETTINGS, indent=4)


def set_configuration(settings: json):
    settings.configuration.SETTINGS = settings
