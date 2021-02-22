import re


def zone_validator(zone_data):
    if not zone_data.get('name'):
        return False, "Name is a required field"
    if not zone_data.get('name').endswith("."):
        return False, "Name must be a canonical name"
    if not zone_data.get("nameserver"):
        return False, "Please provide a nameserver for your zone"
    ns_host = zone_data.get("nameserver")
    if not hostname_validator(ns_host):
        return False, f"nameserver {ns_host} is not a valid hostname"
    if not zone_data.get("rname"):
        return False, "Please provide registered admin email(rname) for your zone"
    email_validator = re.compile(r'^[a-zA-Z0-9_\.\-]+@([a-zA-Z0-9_\-]\.?)+$')
    if not email_validator.search(zone_data.get('rname')):
        return False, "The email in the rname must be a valid email address"
    return True, None


def a_record_validator(record):
    valid, error = content_field_validator(record=record)
    if not valid:
        return valid, error
    ip = record.get('content')
    ip_filter = re.compile(r'^((25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$')
    if not ip_filter.search(ip):
        return False, "Invalid IP Address"
    return True, None


def mx_record_validator(record):
    valid, error = content_field_validator(record=record)
    if not valid:
        return valid, error
    mx_host = record.get('content')
    if not record.get('priority') or not type(record.get('priority')) is int:
        return False, "Expecting an integer value for priority of mx server"
    if not hostname_validator(mx_host):
        return False, "Specify a valid host name for the mail server"
    return True, None


def ns_record_validator(record):
    """
    checks the fields in the ns record for sanity
    :param record:
    :return:
    """
    valid, error = content_field_validator(record=record)
    if not valid:
        return valid, error
    ns_host = record.get("content")
    if not hostname_validator(ns_host):
        return False, "Specify a valid host as a name server"
    return True, None


def cname_validator(record):
    valid, error = content_field_validator(record=record)
    if not valid:
        return valid, error
    cname_host = record.get("content")
    if not hostname_validator(cname_host):
        return False, "Specify a valid host name server"
    return True, None


def txt_record_validator(record):
    valid, error = content_field_validator(record)
    if not valid:
        return valid, error
    return True, None


def content_field_validator(record):
    content_field = record.get("content")
    if not content_field:
        return False, "Content field cannot be empty"
    if not type(content_field) is str:
        return False, "Content field must be a string"
    return True, None


DNS_TYPES = {
    "A": a_record_validator,
    "CNAME": cname_validator,
    "MX": mx_record_validator,
    "NS": ns_record_validator,
    "TXT": txt_record_validator,
}


def hostname_validator(hostname):
    hostname_filter = re.compile(r'^([A-z0-9\-]+.?)+[A-z0-9\-]+$')
    if hostname_filter.search(hostname):
        return True
    return False


def new_record_validator(record_data):
    domain_id = record_data.get("zone_id")
    if not domain_id or type(domain_id) is not int:
        return False, "Zone ID missing or not of type integer"
    record_type = record_data.get("type")
    if not record_type or type(record_type) is not str:
        return False, "Record type missing or not of type String"
    if record_type not in DNS_TYPES.keys():
        return False, "Record type not supported"
    name = record_data.get('name')
    if name and type(name) is not str:
        return False, "Record name is a required field of type string"
    if name and not hostname_validator(name):
        return False, "Name contains illegal characters"
    if record_data.get("ttl") and type(record_data.get("ttl")) is not int:
        return False, "TTL value must be a valid integer"
    if record_data.get("priority") and type(record_data.get("priority")) is not int:
        return False, "Priority value must be a valid integer"
    return True, None
