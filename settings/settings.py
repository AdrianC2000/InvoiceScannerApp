import json

from parsers.json_encoder import JsonEncoder


def get_configuration() -> json:
    f = open('settings/configuration.json', mode="r", encoding="utf-8")
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
        else:
            old_key = key
            new_key = value['value']
            included = value['included']
            invoices_info = change_keys(invoices_info, old_key, new_key, included)

    return dump_to_json(invoices_info)


def remove_null_and_empty_elements(d):
    def empty(x):
        return x is None or x == {} or x == []
    return remove_elements(d, empty, remove_null_and_empty_elements)


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
