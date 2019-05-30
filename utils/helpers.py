import yaml


def yaml_2_json(yaml_file):
    """
    :param yaml_file: file object
    :return: data as dict format
    """
    with open(yaml_file, 'r') as stream:
        try:
            data = yaml.safe_load_all(stream)
        except Exception:
            raise

        res = []
        for doc in data:
            res.append(doc)
    return res
