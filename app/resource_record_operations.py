from flask import request, jsonify

from app import app, db
from app.models import Record, Domain
from app.validators import new_record_validator, DNS_TYPES


def delete_resource_record():
    """
    delete the resource record based on request inputs
    :return: status
    """
    record_id = request.args.get("id")
    if not record_id:
        return {"error": "please provide record id"}
    resource_record = Record.query.filter_by(id=record_id).first()
    if not resource_record:
        return {'error': 'No such resource record exists'}
    if resource_record.type == "SOA":
        return {"error": "Cannot delete SOA record of an active zone. Delete the zone entry to remove it"}
    app.logger.info(f"Deleting the resource record with id:{resource_record.id} and name: {resource_record.name}")
    db.session.delete(resource_record)
    db.session.commit()
    app.logger.info(f"Resource record {resource_record.name} of type {resource_record.type} successfully deleted")
    return {"info": f"Resource record {resource_record.name} of type {resource_record.type} successfully deleted"}


def create_resource_record(req_record_data):
    """
    create a new resource object based on the request parameters
    :param req_record_data:
    :return:
    """
    validation, error = new_record_validator(req_record_data)
    if error:
        return jsonify({'error': error})
    record_type = req_record_data.get('type')
    validation, error = DNS_TYPES[record_type](req_record_data)
    if error:
        return jsonify({"error": error})
    record_id = req_record_data.get('zone_id')
    resource_record = Domain.query.filter_by(id=record_id).first()
    new_record = Record()
    new_record.domain_id = record_id
    if req_record_data.get('name'):
        new_record.name = req_record_data.get("name") + '.' + resource_record.name
    else:
        new_record.name = resource_record.name
    new_record.type = record_type
    new_record.content = req_record_data.get("content")
    new_record.ttl = req_record_data.get("ttl") or 3600
    new_record.prio = req_record_data.get("priority") or None
    db.session.add(new_record)
    db.session.commit()
    return jsonify({"status": "ok"})


def update_resource_record(req_record_data):
    record_id = req_record_data.get('id')
    app.logger.info(f"Modifying record with id {record_id}")
    app.logger.info(f"Checking database for record")
    record = Record.query.filter_by(id=record_id).first()  # Get the record for the ID from the database
    if not record:
        app.logger.error("This record does not exist in the database")
        return jsonify({'error': 'This record id does not exist'})
    record_type = req_record_data.get('type')
    if not record_type or record_type not in DNS_TYPES.keys():
        app.logger.error(f"The record type is missing or not a supported type")
        return jsonify({'error': 'Invalid record type'})
    if not record.type == record_type:
        app.logger.error(f"The record type does not match the existing record")
        return jsonify({'error': 'Record type mismatch'})
    validation, error = DNS_TYPES[record_type](req_record_data)  # check if the validation for the record type
    # passes the function
    if validation:
        update_record(record, req_record_data)
        db.session.commit()
        app.logger.info(f"DNS record with id {record.id} and name {record.name} and type {record.type} "
                        f"updated successfully ")
        return jsonify({'status': 'ok'})
    else:
        return jsonify({"error": error})


def get_resource_records():
    response = []
    record_id = request.args['id']
    if not record_id.isdigit():  # check if the zone id is a numeric value

        return {"error": "zone id must be a numeric value"}
    if not Record.query.filter_by(domain_id=record_id).first():  # check if there are records for the provided zone
        return {"info": "No records for this zone"}
    db_query = Record.query.filter_by(domain_id=record_id)  # Get the resource records for the given domain id
    for value in db_query:
        rrecord = {
            "id": value.id,
            "name": value.name,
            "type": value.type,
            "content": value.content,
            "ttl": value.ttl,
        }
        response.append(rrecord)
    return jsonify(response)


def update_record(record, req_record_data):
    record.content = req_record_data.get('content')
    record.ttl = req_record_data.get('ttl') or record.ttl
    record.prio = req_record_data.get('priority') or record.prio