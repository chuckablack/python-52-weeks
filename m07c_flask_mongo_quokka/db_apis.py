from extensions import db


def remove_internals(d):

    return {k: v for (k, v) in d.items() if not k.startswith("_")}


def get_all_hosts():

    hosts = {host["hostname"]: remove_internals(host) for host in db.hosts.find()}
    return hosts


def set_host(host):

    existing_host = db.hosts.find_one({"hostname": host["hostname"]})
    if not existing_host:
        db.hosts.insert_one(host)
    else:
        db.hosts.update_one({"hostname": host["hostname"]}, {"$set": host})


def get_all_services():

    services = {service["name"]: remove_internals(service) for service in db.services.find()}
    return services


def set_service(service):

    existing_service = db.services.find_one({"name": service["name"]})
    if not existing_service:
        db.services.insert_one(service)
    else:
        db.services.update_one({"name": service["name"]}, {"$set": service})


def get_all_devices():

    devices = {device["name"]: remove_internals(device) for device in db.devices.find()}
    return devices


def set_device(device):

    existing_device = db.devices.find_one({"name": device["name"]})
    if not existing_device:
        db.devices.insert_one(device)
    else:
        db.devices.update_one({"name": device["name"]}, {"$set": device})
