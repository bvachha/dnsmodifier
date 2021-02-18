import json

from flask import request

from app import app
from app.resource_record_operations import delete_resource_record, create_resource_record, update_resource_record, \
    get_resource_records
from app.utilities import api_check
from app.zone_operations import do_zone_build, do_zone_delete, do_zone_get


@app.route('/api/zones/', methods=['GET', 'POST', 'DELETE'])
@api_check
def get_zone_names():
    if request.method == "GET":
        return do_zone_get()
    elif request.method == 'POST':
        return do_zone_build()
    elif request.method == 'DELETE':
        return do_zone_delete()


@app.route('/api/zone-records/', methods=['GET', 'POST', 'DELETE'])
@api_check
def zone_records_operations():
    if request.method == 'GET':
        return get_resource_records()
    elif request.method == 'POST':
        if not request.data:
            return {"error": "Please supply required parameters in json formatting"}
        req_record_data = json.loads(request.data.decode('utf-8'))  # convert json body in bytes to a valid dictionary
        if req_record_data.get("id"):  # If the json body contains an ID then we are probably looking at an update of an
            # existing record
            return update_resource_record(req_record_data)
        else:
            return create_resource_record(req_record_data)
    elif request.method == "DELETE":
        return delete_resource_record()


@app.after_request
def add_header(response):
    """
    add response headers to handle CORS issues with frontend app
    :param response: response object to return
    :return: updated response object with appropriate headers set
    """
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers["Access-Control-Allow-Methods"] = "GET,POST,DELETE"
    response.headers["Access-Control-Allow-Headers"] = "api-key"
    return response
