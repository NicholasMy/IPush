import requests

from ip_sources.ip_source import IpSource


class Ipify(IpSource):
    def get_ipv4(self) -> str:
        return requests.get("https://api.ipify.org?format=json").json().get("ip")

    def get_ipv6(self) -> str:
        return requests.get("https://api6.ipify.org?format=json").json().get("ip")
