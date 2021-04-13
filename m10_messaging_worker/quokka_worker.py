# ---- Worker application --------------------------------

import json
import os

import pika

from CaptureThread import CaptureThread
from PortscanThread import PortscanThread
from TracerouteThread import TracerouteThread

CAPTURE = "capture"
PORTSCAN = "portscan"
TRACEROUTE = "traceroute"

if os.geteuid() != 0:
    exit("You must have root privileges to run this script, try using 'sudo'.")


def start_receiving():

    print(f"Worker: starting rabbitmq, listening for work requests")

    connection = pika.BlockingConnection(pika.ConnectionParameters("localhost"))
    channel = connection.channel()
    worker_queue = "quokka-worker"
    channel.queue_declare(queue=worker_queue, durable=True)
    print(f"\n\n [*] Worker: waiting for messages on queue: {worker_queue}.")

    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(
        on_message_callback=receive_work_request, queue=worker_queue
    )

    try:
        channel.start_consuming()
    except KeyboardInterrupt:
        print(f"\n\n\n---> Worker: shutting down")
        channel.close()
        connection.close()
        exit()



def receive_work_request(capture_channel, method, _, body):

    work_info = json.loads(body)
    if "work_type" not in work_info:
        print(f" !!! Received work request with no work_type: {work_info}")
    if work_info["work_type"] not in [CAPTURE, PORTSCAN, TRACEROUTE]:
        print(f" !!! Received work request for unknown work_type: {work_info['work_type']}")

    print(f"Received work: {work_info['work_type']} full work info: {work_info}")

    capture_channel.basic_ack(delivery_tag=method.delivery_tag)

    process_work_request(work_info["work_type"], work_info)
    print("\n\n [*] Worker: waiting for messages.")


def process_work_request(work_type, work_info):

    if "quokka" not in work_info:
        quokka = "localhost"
    else:
        quokka = work_info["quokka"]

    if work_type == CAPTURE:
        work_thread = CaptureThread(quokka, work_info)
    elif work_type == PORTSCAN:
        work_thread = PortscanThread(quokka, work_info)
    elif work_type == TRACEROUTE:
        work_thread = TracerouteThread(quokka, work_info)
    else:
        print(f" !!! Invalid work_type: {work_type}, should have been caught earlier")
        return

    work_thread.start()


def main():

    start_receiving()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n\n\n---> Worker: shutting down")
        exit()
