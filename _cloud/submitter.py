import requests

ENDPOINT = "http://pythonista.cloud/"


def submit_module(data):
    """Submit a module to the index."""
    req = requests.post(ENDPOINT, json=data)
    req.raise_for_status()
    resp = req.json()

    if not resp["success"]:
        raise ValueError("Something went wrong: '{}: {}'".format(
            resp["error"]["type"], resp["error"]["message"]
        ))

    return req
