from dns_destinations.cloudflare import Cloudflare
from dns_destinations.dns_destination import DnsDestination
from ip_sources.ip_source import IpSource
from ip_sources.ipify import Ipify
from ip_sources.nimy import Nimy
from utils.config_parser import IpushConfig, load_config, Account, DnsService, IpService

if __name__ == '__main__':

    config: IpushConfig = load_config("config.yaml")

    for destination_name, destination in config.destinations.items():
        account: Account = config.accounts.get(destination.account)

        match destination.ip_source:
            case IpService.IPIFY:
                ip_source: IpSource = Ipify()
            case IpService.NIMY:
                ip_source: IpSource = Nimy()
            case _:
                raise ValueError(f"Unknown IP source: {destination.ip_source} ({destination_name})")

        match account.service:
            case DnsService.CLOUDFLARE:
                dns_service: DnsDestination = Cloudflare()
            case _:
                raise ValueError(f"Unknown DNS service: {account.service} ({destination_name})")

        ip: str = ip_source.get_ipv(destination.ip_version)
        success: bool = dns_service.set_ip(account, destination, ip)
