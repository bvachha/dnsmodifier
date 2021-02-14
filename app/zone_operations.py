import json

from flask import request, jsonify
from sqlalchemy.exc import IntegrityError

from app import app, db
from app.models import Domain, Record
from app.validators import zone_validator
from app.zone_record_mappers import build_zone_record, build_zone_ns, build_zone_soa


def do_zone_build():
    if not request.data:
        app.logger.error(f"invalid json parameters sent in request")
        return {"error": "Please supply required parameters in json formatting"}
    json_request = json.loads(request.data.decode('utf-8'))  # convert json body in bytes to a valid dictionary
    error = None
    zone_validation, error = zone_validator(json_request)
    if zone_validation:
        try:
            zone_record = build_zone_record(json_request)
            db.session.add(zone_record)
            db.session.commit()
        except IntegrityError:
            app.logger.error("Attempted to insert duplicate record for zone ")
            error = "This zone name already exists in the database"
            return {"error": error}
        zone_record = Domain.query.filter_by(name=zone_record.name).first()
        if not zone_record:
            app.logger.error("No Zone record found")
        ns_record_list = build_zone_ns(json_request, zone_record.id)
        soa_record = build_zone_soa(json_request, zone_record.id)
        for ns_record in ns_record_list:
            db.session.add(ns_record)
        db.session.add(soa_record)
        db.session.commit()
        return {'status': 'ok'}
    return {"error": error}


def do_zone_delete():
    zone_id = request.args.get("id")
    if not zone_id:
        return {"error": "please provide zone id"}
    zone_record = Domain.query.filter_by(id=zone_id).first()
    if not zone_record:
        return {'error': 'No such zone exists'}
    app.logger.info(f"Deleting the zone with id:{zone_record.id} and name: {zone_record.name}")
    records = Record.query.filter_by(domain_id=zone_record.id)
    for record in records:
        app.logger.info(f"Deleting DNS record: {record.name}")
        db.session.delete(record)
    app.logger.info(f"Deleting DNS Zone record for: {zone_record.name}")
    db.session.delete(zone_record)
    db.session.commit()
    app.logger.info(f"Zone {zone_record.name} successfully deleted")
    return {"info": f"zone {zone_record.name} successfully deleted"}


def do_zone_get():
    response = []
    app.logger.info("Querying the database for zone details")
    db_response = Domain.query.all()
    app.logger.info(f"Found {len(db_response)} records. Returning names")
    for record in db_response:
        zone_record = {
            "id": record.id,
            "name": record.name,
        }
        response.append(zone_record)
    return jsonify(response)
