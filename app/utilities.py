from functools import wraps

from flask import request, jsonify

from app import app


def apicheck(func):
    """
    decorator to check if the api call contains a header with the valid api key and return an error if it fails the check
    :param func: function to be wrapped
    :return: wrapped function
    """
    @wraps(func)
    def wrapper(*args):
        req_api_key = request.headers.get("api-key")
        if not req_api_key or req_api_key != app.config.get("API_KEY"):
            return jsonify({'error': 'Missing or invalid API key'})
        res = func(*args)
        return res
    return wrapper
