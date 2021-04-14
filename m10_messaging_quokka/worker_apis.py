from datetime import datetime
import pika
import json


def start_portscan(target):

    print(f"starting portscan for target: {target}")
    token = str(datetime.now())
    portscan_info = {
        "quokka": "localhost:5001",
        "work_type": "portscan",
        "target": target,
        "token": token,
    }
    portscan_info_json = json.dumps(portscan_info)

    connection = pika.BlockingConnection(pika.ConnectionParameters("localhost"))
    channel = connection.channel()
    channel.queue_declare(queue="quokka-worker", durable=True)
    channel.basic_publish(
        exchange="", routing_key="quokka-worker", body=portscan_info_json
    )

    return token


def start_traceroute(target):

    print(f"starting traceroute for: {target}")

    token = str(datetime.now())
    traceroute_info = {
        "quokka": "localhost:5001",
        "work_type": "traceroute",
        "target": target,
        "token": token,
    }
    traceroute_info_json = json.dumps(traceroute_info)

    connection = pika.BlockingConnection(pika.ConnectionParameters("localhost"))
    channel = connection.channel()
    channel.queue_declare(queue="quokka-worker", durable=True)
    channel.basic_publish(
        exchange="", routing_key="quokka-worker", body=traceroute_info_json
    )

    return token
