import subprocess
from datetime import datetime
from time import sleep

import requests

while True:

    print("\n\n----> Retrieving hosts ...", end="")
    response = requests.get("http://127.0.0.1:5000/hosts")
    if response.status_code != 200:
        print(f" !!!  Failed to retrieve hosts from server: {response.reason}")
        exit()

    print(" Hosts successfully retrieved")

    hosts = response.json()
    # print("\n----- Hosts received (tabulate) --------------------")
    # print("\n", tabulate(sorted(hosts.values(),  key=itemgetter("hostname")), headers="keys"))

    for _, host in hosts.items():

        try:
            print(f"----> Pinging host: {host['hostname']}", end="")
            ping_output = subprocess.check_output(
                ["ping", "-c3", "-n", "-i0.5", "-W2", host["ip"]]
            )
            host["availability"] = True
            host["last_heard"] = str(datetime.now())[:-3]
            print(f" Host ping successful: {host['hostname']}")

        except subprocess.CalledProcessError:
            host["availability"] = False
            print(f" !!!  Host ping failed: {host['hostname']}")

        print(f"----> Updating host status via REST API: {host['hostname']}", end="")
        rsp = requests.put("http://127.0.0.1:5000/hosts", params={"hostname": host["hostname"]}, json=host)
        if rsp.status_code != 204:
            print(
                f"{str(datetime.now())[:-3]}: Error posting to /hosts, response: {rsp.status_code}, {rsp.content}"
            )
            print(f" !!!  Unsuccessful attempt to update host status via REST API: {host['hostname']}")
        else:
            print(f" Successfully updated host status via REST API: {host['hostname']}")

    sleep(15)
