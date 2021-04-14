from scapy2dict import to_dict
from datetime import datetime
import requests
from pprint import pprint, pformat
import scapy.all as scapy


def get_filter(ip, protocol, port):

    capture_filter = ""
    if ip:
        capture_filter += "host " + ip
    if protocol:
        if ip:
            capture_filter += " and " + protocol
        else:
            capture_filter += protocol
        if port:
            capture_filter += " port " + port

    return capture_filter


def get_packets_from_capture(capture):

    packets = list()
    for packet in capture:
        packet_dict = to_dict(packet, strict=True)
        if "Raw" in packet_dict:
            del packet_dict["Raw"]
        packet_dict["hexdump"] = scapy.hexdump(packet, dump=True)
        packet_dict_no_bytes = bytes_to_string(packet_dict)
        packets.append(packet_dict_no_bytes)

        pprint(packet_dict_no_bytes)

    return packets


def send_capture(source, destination, timestamp, packets):

    capture_payload = {
        "source": source,
        "timestamp": timestamp,
        "packets": packets,
    }
    rsp = requests.post(
        "http://" + destination + "/capture/store", json=capture_payload
    )
    if rsp.status_code != 200:
        print(
            f"{str(datetime.now())[:-3]}: Error calling /capture/store response: {rsp.status_code}, {rsp.content}"
        )

    return rsp.status_code


def bytes_to_string(data):

    if isinstance(data, dict):
        for k, v in data.items():
            data[k] = bytes_to_string(v)
        return data
    elif isinstance(data, list):
        for index, v in enumerate(data):
            data[index] = bytes_to_string(v)
        return data
    elif isinstance(data, tuple):
        data_as_list = list(data)
        for index, v in enumerate(data_as_list):
            data_as_list[index] = bytes_to_string(v)
        return tuple(data_as_list)
    elif isinstance(data, bytes):
        return data.decode("latin-1")

    else:
        return data


def send_portscan(source, destination, target, token, timestamp, scan_output):

    portscan_payload = {
        "source": source,
        "target": target,
        "token": token,
        "timestamp": timestamp,
        "scan_output": pformat(scan_output),
    }
    rsp = requests.post(
        "http://" + destination + "/worker/portscan", json=portscan_payload
    )
    if rsp.status_code != 204:
        print(
            f"{str(datetime.now())[:-3]}: Error calling /worker/portscan response: {rsp.status_code}, {rsp.content}"
        )

    return rsp.status_code


def send_traceroute(source, destination, target, token, timestamp, traceroute_graph_bytes):

    portscan_payload = {
        "source": source,
        "target": target,
        "token": token,
        "timestamp": timestamp,
        "traceroute_img": traceroute_graph_bytes,
    }
    rsp = requests.post(
        "http://" + destination + "/worker/traceroute", json=portscan_payload
    )
    if rsp.status_code != 204:
        print(
            f"{str(datetime.now())[:-3]}: Error calling /worker/traceroute response: {rsp.status_code}, {rsp.content}"
        )

    return rsp.status_code
