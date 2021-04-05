import asyncio
import subprocess
from datetime import datetime
from time import time

from hosts_common import discovery, get_hosts


async def ping_host_async(host):

    try:
        ping_cmd = ["ping", "-c3", "-n", "-i0.5", "-W2", host["ip_address"]]
        process = await asyncio.create_subprocess_exec(*ping_cmd, stdout=asyncio.subprocess.PIPE)
        stdout, stderr = await process.communicate()

        if "0 received" in stdout.decode():
            host["availability"] = False
            print(f" !!!  Host ping failed: {host['hostname']}")
        else:
            host["availability"] = True
            host["last_heard"] = str(datetime.now())[:-3]
            print(f"----> Host ping successful: {host['hostname']}")

    except subprocess.CalledProcessError:
        host["availability"] = False
        print(f" !!!  Host ping failed: {host['hostname']}")


def ping_host(host):

    try:
        subprocess.check_output(
            ["ping", "-c3", "-n", "-i0.5", "-W2", host["ip_address"]]
        )
        host["availability"] = True
        host["last_heard"] = str(datetime.now())[:-3]
        print(f"----> Host ping successful: {host['hostname']}")

    except subprocess.CalledProcessError:
        host["availability"] = False
        print(f" !!!  Host ping failed: {host['hostname']}")


async def main():

    # discovery()

    hosts = get_hosts()
    print(f"\n---> Starting to ping {len(hosts)} hosts using asyncio")

    time_start = time()

    # ----- PING USING ASYNCIO --------------------
    ping_hosts = [ping_host_async(host) for host in hosts.values()]
    await asyncio.gather(*ping_hosts)

    ping_with_asyncio_time = time() - time_start
    print(f"---> Completed pinging {len(hosts)} hosts using asyncio, time: {ping_with_asyncio_time:3f}")

    # ----- PING ONE AT A TIME --------------------
    print(f"\n---> Starting to ping {len(hosts)} hosts NOT using asyncio")
    time_start = time()

    for host in hosts.values():
        ping_host(host)

    ping_without_asyncio_time = time() - time_start
    print(f"---> Completed pinging {len(hosts)} hosts NOT using asyncio, time: {ping_without_asyncio_time:3f}")

    print("\nResults:")
    print(f"     Using asyncio:     {ping_with_asyncio_time:>7.3f}")
    print(f"     Not using asyncio: {ping_without_asyncio_time:>7.3f}\n")


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n\nExiting host-monitor")
        exit()
