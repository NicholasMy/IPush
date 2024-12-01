# IPush

A versatile dynamic DNS client that updates DNS records to your current public IP address.

IPush supports multiple domains/subdomains, multiple accounts, Cloudflare proxying, and both IPv4 and IPv6.

## Supported DNS Providers
- [Cloudflare](https://www.cloudflare.com/)
- _More in the future_

## Supported IP Sources
- [Ipify](https://www.ipify.org/)
- _More in the future_

## Installation

IPush is designed to run on Debian-based systems with Python 3.11 or newer, but it should work in other environments too. These steps have been tested on Ubuntu 24.04 with Python 3.12.2.

* `git clone https://github.com/NicholasMy/IPush.git`
* `cd IPush`
* `apt install python3.12-venv`
* `python3 -m venv venv`
* `source venv/bin/activate`
* `pip install -r requirements.txt`
* `touch config.yaml`
* Edit `config.yaml` as described in the [Configuration](#configuration) section below
* Run `python3 ipush.py` to verify it works properly. If it fails, the error will be printed or logged to `logs/ipush.log`
* Note the path to the Python executable within the venv. E.g., `/home/user/IPush/venv/bin/python`
* `crontab -e`
* Add `*/10 * * * * (cd /home/user/IPush && /home/user/IPush/venv/bin/python ipush.py)` to run IPush every 10 minutes. Adjust as needed.
* `tail -f logs/ipush.log` and ensure it runs as scheduled

## Configuration

IPush is configured via `config.yaml` in the project directory.

Here is an example configuration that showcases all of IPush's capabilities:

```yaml
accounts:
  cloudflare1:
    service: cloudflare
    zone_id: 1234
    api_key: abcd
    
destinations:
  destination1:
    account: cloudflare1
    domain: example.com
    subdomain: demo
    ip_source: ipify
    ip_version: 4
    ttl: 600
    proxied: true
```

The `accounts` section is where you'll configure your DNS provider accounts with their API credentials.

* The key of each entry is a unique name for the account. This will be referenced in the `destinations` section below.
* `service` must be "cloudflare" for the time being
* `zone_id` and `api_key` can be retrieved from your DNS provider's website. (See [below](#cloudflare-api-setup) for Cloudflare steps)

The `destinations` section is where you'll configure each domain/subdomain.

* The key of each entry is unique name for the destination, which will be used in logging.
* `account` should be the unique name of one of the accounts you created above
* `domain` should be the apex domain (not a subdomain)
* `subdomain` is optional, and should be ONLY the subdomain portion of the entire domain. If not specified, IPush will update the root domain.
* `ip_source` must be "ipify" for the time being
* `ip_version` can be `4` or `6` to either create an `A` or `AAAA` record respectively.
* `ttl` is the "Time to Live" for the DNS record in seconds (integer)
* `proxied` is an optional boolean (defaults to false) that enables proxying for the DNS record on Cloudflare
    

### Cloudflare API Setup

To get your API credentials for Cloudflare:

* Visit https://dash.cloudflare.com/profile/api-tokens.
* Click "Create token"
* Click "Get started" on "Create Custom Token"
* Name the token something like "IPush Production"
* Under permissions, select "Zone" > "DNS" > "Edit"
* You can restrict API access to a particular Cloudflare "account" or particular zones (domains) if you wish
* Create the token, and copy the token into the IPush configuration as the `api_key`
* Navigate to your "Account home," which lists all of your domains. Click the three dots to the right of a domain, then "Copy zone ID." Paste this as `zone_id` in the config