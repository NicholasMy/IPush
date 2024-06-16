from ip_sources.ip_source import IpSource


class Nimy(IpSource):
    # TODO implement
    def get_ipv4(self) -> str:
        return "127.0.0.1"

    def get_ipv6(self) -> str:
        return "::1"
