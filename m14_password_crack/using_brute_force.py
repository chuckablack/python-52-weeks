import itertools
from time import time, sleep
import argparse
from multiprocessing import Process, Queue

parser = argparse.ArgumentParser(description="Number of processes for brute force")
parser.add_argument("-processes", default=2, help="Number of processes to use")
args = parser.parse_args()
num_processes = int(args.processes)

import psutil
print(f"number of cores: {psutil.cpu_count()}")


def check_password(bf_request_queue, bf_response_queue, bf_terminate_queue):

    while True:

        print(f"oooo waiting for message")
        check_info = bf_request_queue.get()
        print(f"---> received message from queue: {check_info}")

        first_char = check_info["first_char"]
        chars = check_info["chars"]
        pw_length = check_info["pw_length"]
        actual_password = check_info["actual_password"]

        for next_chars in itertools.product(chars, repeat=pw_length-1):
            # print(f"---> constructing password: {first_char} plus {next_chars}")
            test_password = first_char + ''.join(next_chars)
            if test_password == actual_password:
                bf_response_queue.put({"found": True, "pw": test_password, "time": time()})
                break

            if not bf_terminate_queue.empty():
                print(f"~~~~ [{first_char}] terminating as requested")
                bf_response_queue.put({"found": False, "pw": test_password, "time": None})
                break

        else:
            print(f"---! [{first_char}] password not found")
            bf_response_queue.put({"found": False, "pw": test_password, "time": None})

        # bf_response_queue.put({"found": False, "pw": "", "time": time()})
        # print(f"---! Unable to find password of length: {pw_length} starting with {first_char}")


def main():

    bf_request_queue = Queue()
    bf_response_queue = Queue()
    bf_terminate_queue = Queue()

    chars = "0123456789"

    bf_processes = list()
    for proc_num in range(0, num_processes):
        print(f"---> starting process number {proc_num}")
        proc = Process(target=check_password, args=(bf_request_queue, bf_response_queue, bf_terminate_queue))
        proc.start()
        print(f"---> process number {proc_num} started")
        bf_processes.append(proc)

    while True:

        password = input("Password:  ")
        if not password: exit()

        time_start = time()
        for char in chars:

            check_info = dict()
            check_info["first_char"] = char
            check_info["chars"] = chars
            check_info["pw_length"] = len(password)
            check_info["actual_password"] = password

            print(f"---> putting message for char: {char} onto queue: {check_info}")
            bf_request_queue.put(check_info)

        for _ in chars:
            rsp_info = bf_response_queue.get()

            if rsp_info["found"]:
                print(f"---> FOUND PASSWORD: {rsp_info['pw']}")
                print(f"found password in {rsp_info['time']-time_start:.3f}")
                break

        else:
            print(f"---! PASSWORD NOT FOUND: {password}")

        # put a single terminate message in the queue so all process see it and quit
        bf_terminate_queue.put({})
        sleep(1)

        # clear out any excess messages in all the queues
        for queue in [bf_request_queue, bf_response_queue, bf_terminate_queue]:
            while not queue.empty():
                queue.get()

        print(f"request: {bf_request_queue.qsize()}")
        print(f"response: {bf_response_queue.qsize()}")
        print(f"terminate: {bf_terminate_queue.qsize()}")


if __name__ == '__main__':
    main()
