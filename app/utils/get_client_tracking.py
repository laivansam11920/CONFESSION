from flask import request


def get_client_tracking() -> str:

    fingerprint = request.form.get("fingerprint_id")
    ip = request.headers.get("CF-Connecting-IP", request.remote_addr or "127.0.0.1")

    if fingerprint:
        return f"{ip}:{fingerprint}"

    return ip
