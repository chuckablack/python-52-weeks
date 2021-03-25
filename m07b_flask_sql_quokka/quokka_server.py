from flask import Flask, request
from extensions import db


quokka_app = Flask(__name__)
quokka_app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:////tmp/test.db"
quokka_app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(quokka_app)
quokka_app.app_context().push()

# noinspection PyUnresolvedReferences
import db_classes
db.create_all()

from db_apis import get_all_hosts, set_host
from db_apis import get_all_devices, set_device
from db_apis import get_all_services, set_service


@quokka_app.route("/hosts", methods=["GET", "PUT"])
def hosts():

    if request.method == "GET":
        return get_all_hosts()

    elif request.method == "PUT":
        hostname = request.args.get("hostname")
        if not hostname:
            return "must provide hostname on PUT", 400

        host = request.get_json()
        set_host(host)
        return {}, 204


@quokka_app.route("/devices", methods=["GET", "PUT"])
def devices():

    if request.method == "GET":
        return get_all_devices()

    elif request.method == "PUT":
        name = request.args.get("name")
        if not name:
            return "must provide name on PUT", 400

        device = request.get_json()
        set_device(device)
        return {}, 204


@quokka_app.route("/services", methods=["GET", "PUT"])
def services():

    if request.method == "GET":
        return get_all_services()

    elif request.method == "PUT":
        name = request.args.get("name")
        if not name:
            return "must provide name on PUT", 400

        service = request.get_json()
        set_service(service)
        return {}, 204
