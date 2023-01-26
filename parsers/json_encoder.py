from json import JSONEncoder


def beautify_key(prop):
    index = prop.index('__')
    if index <= 0:
        return prop
    return prop[index + 2:]


class JsonEncoder(JSONEncoder):
    """ Class passed to the cls argument of the json.dumps method for json formatting """

    def default(self, o):
        return {beautify_key(k): v for k, v in vars(o).items()}
