from datetime import datetime
import pika
import json


def start_host_portscan(hostname):

    print(f"starting portscan for host: {hostname}")
    token = str(datetime.now())
    portscan_info = {
        "quokka": "localhost:5001",
        "work_type": "portscan",
        "host": hostname,
        "token": token,
    }
    portscan_info_json = json.dumps(portscan_info)

    credentials = pika.PlainCredentials('quokkaUser', 'quokkaPass')
    connection = pika.BlockingConnection(pika.ConnectionParameters(host="localhost", credentials=credentials))
    channel = connection.channel()
    channel.queue_declare(queue="quokka-worker", durable=True)
    channel.basic_publish(
        exchange="", routing_key="quokka-worker", body=portscan_info_json
    )

    return token
