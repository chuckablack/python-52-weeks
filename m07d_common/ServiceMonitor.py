import requests
import time
from dns.resolver import Resolver, Timeout, NXDOMAIN
from ntplib import NTPClient, NTPException
import subprocess


class ServiceMonitor:

    def __init__(self, name, target, data=None):
        self.name = name
        self.target = target
        self.data = data

    def get_status(self):
        raise NotImplementedError("Please implement the get_status() method")


class HttpMonitor(ServiceMonitor):

    def get_status(self):

        time_start = time.time()
        try:
            response = requests.get(self.target)
            if response.status_code == requests.codes.ok:
                return True, time.time()-time_start

        except BaseException as e:
            print(f"!!! Exception in HTTP service monitoring: {repr(e)}")
        return False, 0.0


class DnsMonitor(ServiceMonitor):

    def get_status(self):

        target_resolver = Resolver()
        target_resolver.nameservers = [self.target]

        time_start = time.time()
        try:
            response = target_resolver.query(self.data)
        except NXDOMAIN as e:
            print(f'!!! DNS monitor: nonexistent domain name {self.data}: {e}')
            return False, 0.0
        except Timeout as e:
            print(
                f'!!! DNS monitor: DNS request timed out for {self.target}: {e}'
            )
            return False, 0.0
        except BaseException as e:
            print(f"!!! DNS monitor: Exception occurred: {e}")
            return False, 0.0

        if (
            response is not None
            and response.response is not None
            and len(response.response.answer) > 0
        ):
            return True, time.time()-time_start

        return False,  0.0


class NtpMonitor(ServiceMonitor):

    def get_status(self):

        server = self.target
        c = NTPClient()
        time_start = time.time()
        try:
            c.request(server, version=3)
            return True, time.time()-time_start

        except NTPException as e:
            print(
                f"!!! NTP error encountered for {self.target}, error: {repr(e)}"
            )
            return False, 0.0


class IcmpMonitor(ServiceMonitor):

    def get_status(self):

        try:
            time_start = time.time()
            subprocess.check_output(
                ["ping", "-c3", "-n", "-i0.5", "-W2", self.target]
            )
            return True, time.time()-time_start

        except subprocess.CalledProcessError:
            print(f" !!!  Service ping failed: {self.target}")
            return False, 0.0
