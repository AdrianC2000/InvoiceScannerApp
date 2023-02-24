import json

from settings.settings import get_configuration


class JsonConfigurator:
    __CONFIG_KEYS = ["remove_nulls", "convert_to_cents", "remove_percentage", "convert_currency"]
    __NUMERICAL_KEYS = ["gross_price", "net_price", "net_value", "vat_value", "gross_value"]
    __VAT = ["vat"]
    __CURRENCY = ["currency"]
    __CURRENCIES = {
        "zł": "PLN",
        "zl": "PLN",
        "$": "USD",
        "€": "EUR",
        "£": "GBP"
    }

    def __init__(self, invoices_info: str):
        self.__invoices_info = json.loads(invoices_info)

    def customize_json(self) -> str:
        """ Customize given invoice_info by the currently settings. """
        configuration = get_configuration()['data_configuration']

        for setting_key, setting_value in configuration.items():
            if setting_key in self.__CONFIG_KEYS and setting_value:
                self.__invoices_info = self._process_keyword(setting_key)
            elif setting_key not in self.__CONFIG_KEYS:
                self.__invoices_info = self._process_key_config(setting_key, setting_value)
        return json.dumps(self.__invoices_info)

    def _process_keyword(self, setting_key: str) -> dict:
        return {
            "remove_nulls": self._remove_empty_elements(self.__invoices_info),
            "convert_to_cents": self._convert_to_cents(),
            "remove_percentage": self._remove_percentage(),
            "convert_currency": self._convert_currency()
        }[setting_key]

    def _remove_empty_elements(self, dict_element: dict):
        """ Recursively remove empty lists, empty dicts, or None elements from a dictionary """
        if not isinstance(dict_element, (dict, list)):
            return dict_element
        elif isinstance(dict_element, list):
            return [v for v in (self._remove_empty_elements(v) for v in dict_element) if not self._is_empty(v)]
        else:
            return {k: v for k, v in ((k, self._remove_empty_elements(v)) for k, v in dict_element.items())
                    if not self._is_empty(v)}

    @staticmethod
    def _is_empty(element) -> bool:
        return element is None or element == {} or element == []

    def _convert_to_cents(self):
        """ Convert values like '12.09' or '124,09' to '1209' and '12409' for fixed keys. """
        invoices_info = self._change_value_for_key(self.__invoices_info, ".", "", self.__NUMERICAL_KEYS)
        return self._change_value_for_key(invoices_info, ",", "", self.__NUMERICAL_KEYS)

    def _change_value_for_key(self, dict_element, value_to_remove: str, replacing_value: str, keys: list):
        if isinstance(dict_element, (str, int, float)):
            return dict_element
        if isinstance(dict_element, dict):
            new_element = dict_element.__class__()
            self.replace_value_in_dict(dict_element, keys, new_element, replacing_value, value_to_remove)
        elif isinstance(dict_element, (list, set, tuple)):
            new_element = dict_element.__class__(self._change_value_for_key(v, value_to_remove, replacing_value, keys)
                                                 for v in dict_element)
        else:
            return dict_element
        return new_element

    def replace_value_in_dict(self, dict_element, keys: list, new_element: dict, replacing_value: str,
                              value_to_remove: str):
        for element_key, dict_value in dict_element.items():
            if element_key in keys:
                if dict_value is not None:
                    new_element[element_key] = dict_value.replace(value_to_remove, replacing_value).strip()
                else:
                    new_element[element_key] = dict_value
            else:
                new_element[element_key] = self._change_value_for_key(dict_value, value_to_remove, replacing_value,
                                                                      keys)

    def _remove_percentage(self) -> dict:
        """ Remove percentage from VAT key. """
        return self._change_value_for_key(self.__invoices_info, "%", "", self.__VAT)

    def _convert_currency(self) -> dict:
        """ Convert currency to compatible with ISO 4217. """
        invoices_info = self.__invoices_info
        for currency_key, currency_value in self.__CURRENCIES.items():
            invoices_info = self._change_value_for_key(invoices_info, currency_key, currency_value, self.__CURRENCY)
        return invoices_info

    def _process_key_config(self, old_key: str, key_config: dict) -> dict:
        """ Change key value or remove the key.  """
        new_key = key_config['value']
        included = key_config['included']
        invoices_info = self._replace_key(self.__invoices_info, old_key, new_key, included)
        return invoices_info

    def _replace_key(self, dict_element, old_key: str, new_key: str, included: bool) -> dict:
        if isinstance(dict_element, (str, int, float)):
            return dict_element
        if isinstance(dict_element, dict):
            new_element = dict_element.__class__()
            for element_key, element_value in dict_element.items():
                self.remove_element_or_switch_keys(element_value, new_element, element_key, new_key, included, old_key)
        elif isinstance(dict_element, (list, set, tuple)):
            new_element = dict_element.__class__(
                self._replace_key(dict_value, old_key, new_key, included) for dict_value in dict_element)
        else:
            return dict_element
        return new_element

    def remove_element_or_switch_keys(self, element_value, new_element, element_key: str, new_key: str, included: bool,
                                      old_key: str):
        if element_key == old_key and included:
            new_element[new_key] = self._replace_key(element_value, old_key, new_key, included)
        elif element_key != old_key:
            new_element[element_key] = self._replace_key(element_value, old_key, new_key, included)
