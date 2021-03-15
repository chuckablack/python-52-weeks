import json
import yaml
import csv
from flask import Flask, request
import napalm


app = Flask(__name__)


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
