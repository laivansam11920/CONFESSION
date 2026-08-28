from flask import request


def get_client_ip() -> str:

    return request.headers.get("CF-Connecting-IP", request.remote_addr or "127.0.0.1")
