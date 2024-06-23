from typing import Any

import requests

from dns_destinations.dns_destination import DnsDestination
from utils.config_parser import Account, Destination
from utils.logging import get_app_logger

logger = get_app_logger(__name__)


class Cloudflare(DnsDestination):
    def set_ip(self, account: Account, destination: Destination, ip: str) -> bool:
        # Updates an existing record if it exists, otherwise creates a new record

        record_type: str = "A" if destination.ip_version == 4 else "AAAA"
        name: str = f"{destination.subdomain}.{destination.domain}" if destination.subdomain else destination.domain

        headers: dict[str, str] = {
            "Authorization": f"Bearer {account.api_key}",
        }

        body: dict[str, Any] = {
            "type": record_type,
            "name": name,
            "content": ip,
            "ttl": destination.ttl,
            "proxied": destination.proxied
        }

        def get_existing_record_id() -> str | None:
            url: str = f"https://api.cloudflare.com/client/v4/zones/{account.zone_id}/dns_records"
            params: dict[str, str] = {
                "type": record_type,
                "name": name
            }
            response = requests.get(url, headers=headers, params=params).json()
            if response.get("success", False):
                if records := response.get("result", False):
                    return records[0]["id"]
            return None

        def create_new_dns_record() -> bool:
            url: str = f"https://api.cloudflare.com/client/v4/zones/{account.zone_id}/dns_records"
            response: dict = requests.post(url, headers=headers, json=body).json()
            success: bool = response.get("success", False)
            if not success:
                logger.warning(response)
            return success

        def update_existing_dns_record(record_id: str) -> bool:
            url: str = f"https://api.cloudflare.com/client/v4/zones/{account.zone_id}/dns_records/{record_id}"
            response: dict = requests.put(url, headers=headers, json=body).json()
            success: bool = response.get("success", False)
            if not success:
                logger.warning(response)
            return success

        logger.debug("Checking for existing DNS record in Cloudflare")
        existing_record_id: str | None = get_existing_record_id()
        if existing_record_id:
            logger.debug(f"Updating existing record {record_type} {name} -> {ip}")
            success: bool = update_existing_dns_record(existing_record_id)
        else:
            logger.debug(f"No existing record found. Creating a new one {record_type} {name} -> {ip}")
            success: bool = create_new_dns_record()

        return success
