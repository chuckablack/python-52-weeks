from db_classes import db, Host, Service, Device


def get_as_dict(model_obj):

    return {k: v for (k, v) in model_obj.__dict__.items() if not k.startswith("_")}


def get_all_hosts():

    host_objs = db.session.query(Host).all()
    hosts = {host_obj.hostname: get_as_dict(host_obj) for host_obj in host_objs}
    return hosts


def set_host(host):

    host_obj = db.session.query(Host).filter_by(hostname=host["hostname"]).one_or_none()
    if not host_obj:
        host_obj = Host(**host)
        db.session.add(host_obj)
    else:
        if "ip_address" in host:
            host_obj.ip_address = host["ip_address"]
        if "mac_address" in host:
            host_obj.mac_address = host["mac_address"]
        if "availability" in host:
            host_obj.availability = host["availability"]
        if "response_time" in host:
            host_obj.response_time = host["response_time"]
        if "last_heard" in host:
            host_obj.last_heard = host["last_heard"]

    db.session.commit()


def get_all_services():

    service_objs = db.session.query(Service).all()
    services = {service_obj.name: get_as_dict(service_obj) for service_obj in service_objs}
    return services


def set_service(service):

    service_obj = db.session.query(Service).filter_by(name=service["name"]).one_or_none()
    if not service_obj:
        service_obj = Service(**service)
        db.session.add(service_obj)
    else:
        if "target" in service:
            service_obj.target = service["target"]
        if "data" in service:
            service_obj.data = service["data"]
        if "availability" in service:
            service_obj.availability = service["availability"]
        if "response_time" in service:
            service_obj.response_time = service["response_time"]
        if "last_heard" in service:
            service_obj.last_heard = service["last_heard"]

    db.session.commit()


def get_all_devices():

    device_objs = db.session.query(Device).all()
    devices = {device_obj.name: get_as_dict(device_obj) for device_obj in device_objs}
    return devices


def set_device(device):

    device_obj = db.session.query(Device).filter_by(name=device["name"]).one_or_none()
    if not device_obj:
        device_obj = Device(**device)
        db.session.add(device_obj)
    else:
        if "ip_address" in device:
            device_obj.target = device["ip_address"]
        if "model" in device:
            device_obj.model = device["model"]
        if "os_version" in device:
            device_obj.os_version = device["os_version"]
        if "availability" in device:
            device_obj.availability = device["availability"]
        if "response_time" in device:
            device_obj.response_time = device["response_time"]
        if "last_heard" in device:
            device_obj.last_heard = device["last_heard"]

    db.session.commit()
