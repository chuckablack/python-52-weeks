import json
from flask import Flask, request
from m02_files.inventory import get_inventory
import napalm


app = Flask(__name__)


@app.route("/inventory")
def inventory():
    return json.dumps(get_inventory())


@app.route("/interface_counters")
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


@app.route("/device_status")
def device_status():
    return "Hello, Device Status!"


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
