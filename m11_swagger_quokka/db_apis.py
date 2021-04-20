from extensions import db
from datetime import datetime
import time


def remove_internals(d):

    return {k: v for (k, v) in d.items() if not k.startswith("_")}


def get_all_hosts():

    hosts = {host["hostname"]: remove_internals(host) for host in db.hosts.find()}
    return hosts


def get_host(hostname):

    host = db.hosts.find_one({"hostname": hostname})
    return remove_internals(host)


def set_host(host):

    existing_host = db.hosts.find_one({"hostname": host["hostname"]})
    if not existing_host:
        db.hosts.insert_one(host)
    else:
        db.hosts.update_one({"hostname": host["hostname"]}, {"$set": host})


def get_portscan(target, token):

    max_wait_time = 300  # extended port scan allowed to take 5 minutes max
    start_time = datetime.now()
    while (datetime.now() - start_time).total_seconds() < max_wait_time:

        # print(f"searching db for target: {target}, token: {token}")
        scan = db.portscans.find_one({"target": target, "token": token})
        if not scan:
            time.sleep(5)
            continue

        # print(f"found it, returning scan: {scan}")
        return remove_internals(scan)

    return {}  # portscan results never found


def get_traceroute(target, token):

    max_wait_time = 300  # extended port scan allowed to take 5 minutes max
    start_time = datetime.now()
    while (datetime.now() - start_time).total_seconds() < max_wait_time:

        # print(f"searching db for target: {target}, token: {token}")
        traceroute = db.traceroutes.find_one({"target": target, "token": token})
        if not traceroute:
            time.sleep(5)
            continue

        # print(f"found it, returning traceroute: {traceroute}")
        return remove_internals(traceroute)

    return {}  # traceroute results never found


def get_all_services():

    services = {service["name"]: remove_internals(service) for service in db.services.find()}
    return services


def get_service(name):

    service = db.services.find_one({"name": name})
    return remove_internals(service)


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


def record_portscan_data(portscan_data):

    db.portscans.insert_one(portscan_data)


def record_traceroute_data(traceroute_data):

    db.traceroutes.insert_one(traceroute_data)
