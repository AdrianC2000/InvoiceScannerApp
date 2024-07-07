from json import JSONEncoder


class JsonEncoder(JSONEncoder):
    """ Class passed to the cls argument of the json.dumps method for json formatting """

    def default(self, o):
        return {self._beautify_key(k): v for k, v in vars(o).items()}

    @staticmethod
    def _beautify_key(prop):
        try:
            index = prop.index('__')
            if index <= 0:
                return prop
            return prop[index + 2:]
        except ValueError:
            return prop
