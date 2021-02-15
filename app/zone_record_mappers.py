from app.models import Domain, Record
from app.parsers import parse_soa_email


def build_zone_record(zone_data):
    """
    build the zone record from the given zone data.
    :param zone_data: dict containing the body of the request
    :return: zone record object
    """
    zone_record = Domain()
    zone_record.name = zone_data['name'].rstrip(".")
    zone_record.type = 'NATIVE'
    return zone_record


def build_zone_ns(zone_data, zone_id):
    """
    function to handle the nameserver insertions coming in through the zone creation endpoint
    :param zone_data: dictionary containing the zone creation data
    :param zone_id: zone id value that the ns record maps to
    :return: list of nameserver records
    """
    nameservers = []
    for ns_value in zone_data['nameservers']:
        ns_record = Record()
        ns_record.domain_id = zone_id
        ns_record.name = zone_data['name'].rstrip(".")
        ns_record.type = "NS"
        ns_record.content = ns_value
        ns_record.ttl = 3600
        nameservers.append(ns_record)
    return nameservers


def build_zone_soa(zone_data, zone_id):
    """
    build the SOA record for the zone from the zone creation data
    :param zone_id: id of the zone record to map the resource record to
    :param zone_data:incoming zone data dictionary
    :return: record object for the SOA record
    """
    nameserver = zone_data['nameservers'][0]
    soa_record = Record()
    soa_record.domain_id = zone_id
    soa_record.name = zone_data['name'].rstrip(".")
    rname = parse_soa_email(email=zone_data['rname'], encode=True)
    soa_record.type = "SOA"
    soa_record.content = f"{nameserver} {rname} 1 86400 7200 3600000 3600"
    soa_record.ttl = 3600
    return soa_record
