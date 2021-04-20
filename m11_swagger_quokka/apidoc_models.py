from flask_restx import Api, fields


class ApiModels:

    host_fields = None
    device_fields = None
    service_fields = None
    hosts_response = None
    devices_response = None
    services_response = None
    token_response = None
    portscan_data = None
    traceroute_data = None

    @staticmethod
    def set_api_models(api: Api):

        ApiModels.host_fields = api.model(
            "Host Fields",
            {
                "ip_address": fields.String(example="192.168.254.14"),
                "mac_address": fields.String(example="00:27:02:15:5c:d5"),
                "hostname": fields.String(example="RokuStreamingStick.home"),
                "last_heard": fields.String(example="2021-04-19 14:42:15.185"),
                "availability": fields.Boolean(example="true"),
                "response_time": fields.Integer(example="0.005"),
            },
        )
        ApiModels.device_fields = api.model(
            "Device Fields",
            {
                "ip_address": fields.String(example="64.103.37.51"),
                "name": fields.String(example="CSR-sandbox"),
                "hostname": fields.String(example="ios-xe-mgmt.cisco.com"),
                "vendor": fields.String(example="cisco"),
                "model": fields.String(example="CSR1000V"),
                "os": fields.String(example="iosxe"),
                "os_version": fields.String(example="16.9.3"),
                "last_heard": fields.String(example="2021-04-19 14:43:41.106"),
                "availability": fields.Boolean(example="true"),
                "response_time": fields.Integer(example="7.886"),
            },
        )
        ApiModels.service_fields = api.model(
            "Service Fields",
            {
                "name": fields.String(example="HTTP davidbombal"),
                "type": fields.String(example="https"),
                "target": fields.String(example="http://www.davidbombal.com"),
                "data": fields.String(example=""),
                "last_heard": fields.String(example="2021-04-19 14:43:46.102"),
                "availability": fields.Boolean(example="true"),
                "response_time": fields.Integer(example="1.525"),
            },
        )
        ApiModels.hosts_response = api.model(
            "Hosts Response",
            {
                "hostname": fields.Nested(ApiModels.host_fields)
            }
        )
        ApiModels.devices_response = api.model(
            "Devices Response",
            {
                "name": fields.Nested(ApiModels.device_fields)
            }
        )
        ApiModels.services_response = api.model(
            "Services Response",
            {
                "name": fields.Nested(ApiModels.service_fields)
            }
        )
        ApiModels.token_response = api.model(
            "Token Response",
            {
                "token": fields.String(example="2021-04-20 14:06:35.074948"),
            }
        )
        ApiModels.portscan_data = api.model(
            "Portscan Data",
            {
                "source": fields.String(example="quokka"),
                "target": fields.String(example="Google-Home.home"),
                "token": fields.String(example="2021-04-20 14:06:35.074948"),
                "timestamp": fields.String(example="2021-04-20 14:06:38.72534"),
                "scan_output": fields.String(example="{'nmap': {'command_line': 'nmap..."),
            }
        )
        ApiModels.traceroute_data = api.model(
            "Traceroute Data",
            {
                "source": fields.String(example="quokka"),
                "target": fields.String(example="www.google.com"),
                "token": fields.String(example="2021-04-20 14:16:21.311400"),
                "timestamp": fields.String(example="2021-04-20 14:16:24.93611"),
                "traceroute_img": fields.String(example="iVBORw0KGgoAAAANSUhEU..."),
            }
        )
