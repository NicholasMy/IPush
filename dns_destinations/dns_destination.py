from utils.config_parser import Destination, Account


class DnsDestination:
    def set_ip(self, account: Account, destination: Destination, ip: str) -> bool:
        raise NotImplementedError
