from enum import Enum
import yaml
from pydantic import BaseModel, field_validator


class IpService(Enum):
    NIMY = "nimy"
    IPIFY = "ipify"


class DnsService(Enum):
    CLOUDFLARE = "cloudflare"


class Account(BaseModel):
    service: DnsService
    zone_id: str | None = None
    api_key: str | None = None


class Destination(BaseModel):
    account: str
    domain: str
    subdomain: str | None = None
    ip_source: IpService
    ip_version: int
    ttl: int
    proxied: bool = False

    @field_validator("ip_version")
    @classmethod
    def validate_ip_version(cls, v: int):
        assert v in {4, 6}, f"Invalid IP version: {v}"
        return v


class IpushConfig(BaseModel):
    accounts: dict[str, Account]
    destinations: dict[str, Destination]


def load_config(config_file: str) -> IpushConfig:
    with open(config_file, "r") as f:
        return IpushConfig.model_validate(yaml.safe_load(f.read()))
