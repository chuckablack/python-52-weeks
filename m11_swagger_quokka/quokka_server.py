from flask import Flask, request
from flask_cors import CORS
from flask_restx import Api, Resource
from quokka_server_utils import fix_target

from apidoc_models import ApiModels

quokka_app = Flask(__name__)
CORS(quokka_app)

api = Api(quokka_app, version="1.0", title="Quokka", description="Quokka implementation")
ApiModels.set_api_models(api)

from db_apis import get_all_hosts, set_host, get_portscan
from db_apis import get_all_devices, set_device
from db_apis import get_all_services, set_service, get_traceroute

from db_apis import record_portscan_data, record_traceroute_data
from worker_apis import start_portscan, start_traceroute


@api.route("/hosts", methods=["GET", "PUT"])
@api.doc()
class HostsEndpoint(Resource):
    @staticmethod
    @api.response(200, 'Success', ApiModels.hosts_response)
    def get():
        return get_all_hosts()

    @staticmethod
    @api.doc(params={"hostname": "hostname of host to add or update"}, body=ApiModels.host_fields)
    @api.response(204, 'Success')
    @api.response(404, 'must provide hostname on PUT')
    def put():
        hostname = request.args.get("hostname")
        if not hostname:
            return "must provide hostname on PUT", 400

        host = request.get_json()
        set_host(host)
        return {}, 204


@api.route("/devices", methods=["GET", "PUT"])
class DevicesEndpoint(Resource):
    @staticmethod
    @api.response(200, 'Success', ApiModels.devices_response)
    def get():
        return get_all_devices()

    @staticmethod
    @api.doc(params={"name": "name of device to add or update"}, body=ApiModels.device_fields)
    @api.response(204, 'Success')
    @api.response(404, 'must provide name on PUT')
    def put():
        name = request.args.get("name")
        if not name:
            return "must provide name on PUT", 400

        device = request.get_json()
        set_device(device)
        return {}, 204


@api.route("/services", methods=["GET", "PUT"])
class ServicesEndpoint(Resource):
    @staticmethod
    @api.response(200, 'Success', [ApiModels.service_fields])
    def get():
        return get_all_services()

    @staticmethod
    @api.doc(params={"name": "name of service to add or update"}, body=ApiModels.service_fields)
    @api.response(204, 'Success')
    @api.response(404, 'must provide name on PUT')
    def put():
        name = request.args.get("name")
        if not name:
            return "must provide name on PUT", 400

        service = request.get_json()
        set_service(service)
        return {}, 204


@api.route("/scan", methods=["GET", "POST"])
class ScanEndpoint(Resource):
    @staticmethod
    @api.doc(params={"token": "the token returned from the corresponding POST that initiated the portscan"})
    @api.response(200, 'Success', ApiModels.portscan_data)
    @api.response(400, "must provide token and target to get portscan")
    def get():
        target = request.args.get("target")
        if not target:
            return "must provide target to get portscan", 400
        token = request.args.get("token")
        if not token:
            return "must provide token to get portscan", 400

        return get_portscan(target, token)

    @staticmethod
    @api.doc(params={"target": "IP address or hostname of target host or device to scan"})
    @api.response(200, 'Success', ApiModels.token_response)
    @api.response(400, 'must provide target to get portscan')
    def post():
        target = request.args.get("target")
        if not target:
            return "must provide target to get portscan", 400
        token = start_portscan(target)
        return {"token": token}


@api.route("/worker/portscan", methods=["POST"])
class WorkerScanEndpoint(Resource):
    @staticmethod
    @api.doc(body=ApiModels.portscan_data)
    @api.response(204, 'Success')
    def post():
        portscan_data = request.get_json()
        record_portscan_data(portscan_data)

        return {}, 204


@api.route("/traceroute", methods=["GET", "POST"])
class TracerouteEndpoint(Resource):
    @staticmethod
    @api.doc(params={"token": "the token returned from the corresponding POST that initiated the traceroute",
                     "target": "the target for the traceroute request"})
    @api.response(400, "must provide token and target to get traceroute")
    @api.response(200, 'Success', ApiModels.traceroute_data)
    def get():

        target = request.args.get("target")
        if not target:
            return "must provide service target to get traceroute", 400
        target = fix_target(target)

        token = request.args.get("token")
        if not token:
            return "must provide token to get traceroute", 400
        return get_traceroute(target, token)

    @staticmethod
    @api.doc(params={"target": "IP address or hostname of target service, host, or device to find traceroute for"})
    @api.response(200, 'Success', ApiModels.token_response)
    @api.response(400, 'must provide target to initiate traceroute')
    def post():
        target = request.args.get("target")
        if not target:
            return "must provide  target to get traceroute", 400
        target = fix_target(target)

        token = start_traceroute(target)
        return {"token": token}


@api.route("/worker/traceroute", methods=["POST"])
class WorkerTracerouteEndpoint(Resource):
    @staticmethod
    @api.doc(body=ApiModels.traceroute_data)
    @api.response(204, 'Success')
    def post():
        traceroute_data = request.get_json()
        record_traceroute_data(traceroute_data)

        return {}, 204
