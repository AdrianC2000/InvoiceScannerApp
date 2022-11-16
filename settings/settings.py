import json

from parsers.json_encoder import JsonEncoder

NUMERICAL_KEYS = ["gross_price", "net_price", "net_value", "vat_value", "gross_value"]
VAT = ["vat"]
CURRENCY = ["currency"]
CURRENCIES = {
    "zł": "PLN",
    "zl": "PLN",
    "$": "USD",
    "€": "EUR",
    "£": "GBP"
}


def get_configuration() -> json:
    with open('settings/configuration.json', mode="r", encoding="utf-8") as f:
        return json.load(f)


def set_configuration(settings_json: json):
    with open('settings/configuration.json', 'w') as settings_file:
        settings_file.write(settings_json)


def customize_json(invoices_info: str) -> str:
    configuration = get_configuration()['data_configuration']
    invoices_info = json.loads(invoices_info)

    for key, value in configuration.items():
        if key == 'remove_nulls':
            if value:
                invoices_info = remove_null_and_empty_elements(invoices_info)
        elif key == 'convert_to_cents':
            if value:
                invoices_info = change_value_for_key(invoices_info, ".", "", NUMERICAL_KEYS)
                invoices_info = change_value_for_key(invoices_info, ",", "", NUMERICAL_KEYS)
        elif key == 'remove_percentage':
            if value:
                invoices_info = change_value_for_key(invoices_info, "%", "", VAT)
        elif key == 'convert_currency':
            if value:
                for k in CURRENCIES.keys():
                    temp = invoices_info
                    invoices_info = change_value_for_key(invoices_info, k, CURRENCIES[k], CURRENCY)
                    if temp != invoices_info:
                        break
        elif key != 'remove_percentage':
            old_key = key
            new_key = value['value']
            included = value['included']
            invoices_info = change_keys(invoices_info, old_key, new_key, included)

    return dump_to_json(invoices_info)


def remove_null_and_empty_elements(d):
    def empty(x):
        return x is None or x == {} or x == []

    return remove_elements(d, empty, remove_null_and_empty_elements)


def change_value_for_key(obj, value_to_remove, replacing_value, keys):
    if isinstance(obj, (str, int, float)):
        return obj
    if isinstance(obj, dict):
        new = obj.__class__()
        for k, v in obj.items():
            if k in keys:
                if v is not None:
                    new[k] = v.replace(value_to_remove, replacing_value).replace(" ", "")
                else:
                    new[k] = v
            else:
                new[k] = change_value_for_key(v, value_to_remove, replacing_value, keys)
    elif isinstance(obj, (list, set, tuple)):
        new = obj.__class__(change_value_for_key(v, value_to_remove, replacing_value, keys) for v in obj)
    else:
        return obj
    return new


def remove_empty_elements(d):
    def empty(x):
        return x == {} or x == []

    return remove_elements(d, empty, remove_empty_elements)


def remove_elements(d, empty, further_function):
    if not isinstance(d, (dict, list)):
        return d
    elif isinstance(d, list):
        return [v for v in (further_function(v) for v in d) if not empty(v)]
    else:
        return {k: v for k, v in ((k, further_function(v)) for k, v in d.items()) if not empty(v)}


def change_keys(obj: json, old_key: str, new_key: str, included: bool) -> dict:
    if isinstance(obj, (str, int, float)):
        return obj
    if isinstance(obj, dict):
        new = obj.__class__()
        for k, v in obj.items():
            if k == old_key and included:
                new[new_key] = remove_empty_elements(change_keys(v, old_key, new_key, included))
            elif k != old_key:
                new[k] = remove_empty_elements(change_keys(v, old_key, new_key, included))
    elif isinstance(obj, (list, set, tuple)):
        new = obj.__class__(remove_empty_elements(change_keys(v, old_key, new_key, included) for v in obj))
    else:
        return obj
    return new


def dump_to_json(obj) -> json:
    return json.dumps(obj, indent=4, cls=JsonEncoder, ensure_ascii=False)
