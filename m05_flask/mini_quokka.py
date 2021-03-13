import json
import yaml
import csv
from flask import Flask, request
import napalm


app = Flask(__name__)

# READ THIS: Don't do this. By that I mean, don't use global variables in a flask application.
#            The reason: flask is by nature, multi-threaded. Each REST request will operate on
#            it's own thread. So you could have multiple threads attempting to write global data.
#            That's a bad, bad idea.
#            In the next lessons, we'll be replacing this data with an SQL database. And reads
#            and writes to the database are safe.

# DON'T DO THIS # DON'T DO THIS # DON'T DO THIS !!!
global_devices = dict()  # not thread-safe (flask)
global_hosts = dict()  # not thread-safe (flask)
global_services = dict()  # not thread-safe (flask)
# DON'T DO THIS # DON'T DO THIS # DON'T DO THIS !!!


@app.route("/inventory", methods=["GET"])
def inventory():

    inventory_file_type = request.args.get("type")

    if inventory_file_type.lower() == 'yaml':
        with open("inventory.yaml", "r") as yaml_in:
            yaml_inventory = yaml_in.read()
            return {"inventory": yaml.safe_load(yaml_inventory)}

    elif inventory_file_type.lower() == 'json':
        with open("inventory.json", "r") as json_in:
            return {"inventory": json.loads(json_in.read())}

    elif inventory_file_type.lower() == 'csv':
        with open("inventory.csv", "r") as csv_in:
            csv_reader = csv.DictReader(csv_in)
            csv_inventory = list()
            for device in csv_reader:
                csv_inventory.append(device)
            return {"inventory": csv_inventory}

    else:
        return "missing or invalid type, should be yaml, json, or csv", 400


@app.route("/interface_counters", methods=["GET"])
def interface_counters():

    device_name = request.args.get("device")
    device_type = request.args.get("type")
    port = request.args.get("port")
    username = request.args.get("username")
    password = request.args.get("password")

    result, data = get_intf_counters(
        device_name=device_name,
        device_type=device_type,
        credentials={"username": username, "password": password},
        port=int(port),
    )
    if result != "success":
        return data, 406
    else:
        return data, 200


@app.route("/hosts", methods=["GET", "POST", "PUT", "DELETE"])
def hosts():
    global global_hosts  # Remember, don't do this (use globals in Flask)

    if request.method == "GET":
        return global_hosts

    elif request.method == "POST":
        global_hosts = dict()
        global_hosts = request.get_json()
        return {}, 204

    elif request.method == "PUT":
        hostname = request.args.get("hostname")
        if not hostname:
            return "must provide hostname on PUT", 400

        host = request.get_json()
        global_hosts[hostname] = host
        return {}, 204

    elif request.method == "DELETE":
        hostname = request.args.get("hostname")
        if not hostname:
            return "must provide hostname on DELETE", 400

        del global_hosts[hostname]
        return {}, 204


def get_intf_counters(device_name, device_type, port, credentials):

    if device_type == "csr":
        driver = napalm.get_network_driver("ios")
    else:
        return "error", "getting counters supported only for CSR devices"

    device = driver(
        hostname=device_name,
        username=credentials["username"],
        password=credentials["password"],
        optional_args={"port": port},
    )

    device.open()
    counters = device.get_interfaces_counters()
    return "success", json.dumps(counters)


if __name__ == "__main__":
    app.run()
