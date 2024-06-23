from dns_destinations.cloudflare import Cloudflare
from dns_destinations.dns_destination import DnsDestination
from ip_sources.ip_source import IpSource
from ip_sources.ipify import Ipify
from ip_sources.nimy import Nimy
from utils.config_parser import IpushConfig, load_config, Account, DnsService, IpService
from utils.logging import configure_logging, get_app_logger

if __name__ == '__main__':

    configure_logging()
    logger = get_app_logger(__name__)
    config: IpushConfig = load_config("config.yaml")
    logger.debug("Loaded config")

    for destination_name, destination in config.destinations.items():
        try:
            logger.info(f"Beginning destination {destination_name}")
            account: Account = config.accounts.get(destination.account)

            match destination.ip_source:
                case IpService.IPIFY:
                    ip_source: IpSource = Ipify()
                    logger.info("Using Ipify as IP source")
                case IpService.NIMY:
                    ip_source: IpSource = Nimy()
                    logger.info("Using Nimy as IP source")
                case _:
                    raise ValueError(f"Unknown IP source: {destination.ip_source} ({destination_name})")

            match account.service:
                case DnsService.CLOUDFLARE:
                    dns_service: DnsDestination = Cloudflare()
                case _:
                    raise ValueError(f"Unknown DNS service: {account.service} ({destination_name})")

            ip: str = ip_source.get_ipv(destination.ip_version)
            logger.info(f"Current IP address is {ip}")
            success: bool = dns_service.set_ip(account, destination, ip)
            if success:
                logger.info(f"Successfully updated {destination_name}")
        except Exception as e:
            logger.error(f"Exception while processing destination {destination_name}: {e}")
