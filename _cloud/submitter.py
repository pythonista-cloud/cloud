import requests

ENDPOINT = "http://pythonista.cloud/"


def submit_module(data):
    """Submit a module to the index."""
    r = requests.post(ENDPOINT, json=data)
    r.raise_for_status()
    resp = r.json()
    if not resp["success"]:
        raise ValueError("Something went wrong: '{}: {}'".format(
            resp["error"]["type"], resp["error"]["message"]
        ))
        pass
    return r

