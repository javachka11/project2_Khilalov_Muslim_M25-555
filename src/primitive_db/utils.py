import json


def load_metadata(filepath):
    d = None
    try:
        fp = open(filepath, 'r')
    except FileNotFoundError:
        d = dict()
    else:
        d = json.load(fp)
        fp.close()
    return d


def save_metadata(filepath, data):
    with open(filepath, 'w+') as fp:
        json.dump(data, fp)
