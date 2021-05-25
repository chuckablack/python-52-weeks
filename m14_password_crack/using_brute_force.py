import itertools
from time import time, sleep
import argparse
from multiprocessing import Process, Queue
import psutil
import sys

parser = argparse.ArgumentParser(description="brute force password crack")
parser.add_argument("-P", "--processes", default=psutil.cpu_count(), help="Number of processes to use")
parser.add_argument("-N", "--numeric", default=True, help="Whether to use numerics", action="store_true")
parser.add_argument("-A", "--alpha", default=False, help="Whether to use alphabetic", action="store_true")
parser.add_argument("-S", "--special", default=False, help="Whether to use special chars", action="store_true")

args = parser.parse_args()
num_processes = int(args.processes)
numeric = args.numeric
alpha = args.alpha
special = args.special


def check_password(bf_request_queue, bf_response_queue, bf_terminate_queue):

    while True:

        check_info = bf_request_queue.get()

        if "exit" in check_info:
            break

        first_char = check_info["first_char"]
        chars = check_info["chars"]
        pw_length = check_info["pw_length"]
        actual_password = check_info["actual_password"]

        for next_chars in itertools.product(chars, repeat=pw_length-1):
            test_password = first_char + ''.join(next_chars)

            # sys.stdout.write("\r")
            # sys.stdout.write(f"-- testing: {test_password}")

            if test_password == actual_password:
                bf_response_queue.put({"found": True, "pw": actual_password, "time": time()})
                break

            if not bf_terminate_queue.empty():
                bf_response_queue.put({"found": False, "pw": actual_password, "time": None})
                break

        else:
            bf_response_queue.put({"found": False, "pw": actual_password, "time": None})


def main():

    bf_request_queue = Queue()
    bf_response_queue = Queue()
    bf_terminate_queue = Queue()

    chars = ""
    if numeric: chars += "0123456789"
    if alpha:   chars += "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
    if special: chars += "`~!@#$%^&*(_-+={[}]|\\:;\"\'<,>.?/"

    print(f"\nsearch characters: {chars}\n")
    bf_processes = list()
    for proc_num in range(0, num_processes):
        proc = Process(target=check_password, args=(bf_request_queue, bf_response_queue, bf_terminate_queue))
        proc.start()
        print(f"---> process number {proc_num} started")
        bf_processes.append(proc)

    while True:

        password = input("\nPassword:  ")
        if not password:
            for _ in bf_processes:
                bf_request_queue.put({"exit": True})
            print("\n... exiting brute force password finder")
            break

        time_start = time()
        for char in chars:

            check_info = dict()
            check_info["first_char"] = char
            check_info["chars"] = chars
            check_info["pw_length"] = len(password)
            check_info["actual_password"] = password

            bf_request_queue.put(check_info)

        for _ in chars:
            rsp_info = bf_response_queue.get()

            if rsp_info["found"]:
                print(f"\n---> FOUND PASSWORD: {rsp_info['pw']}")
                print(f"   +---> found password in {rsp_info['time']-time_start:.3f}")
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

        print("\nQueues:")
        print(f"-- request: {bf_request_queue.qsize()}")
        print(f"-- response: {bf_response_queue.qsize()}")
        print(f"-- terminate: {bf_terminate_queue.qsize()}")


if __name__ == '__main__':
    main()
