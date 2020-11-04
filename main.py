import os

import requests
from dotenv import load_dotenv

load_dotenv()

GANDI_DOMAIN = os.getenv("GANDI_DOMAIN")
GANDI_SUBDOMAIN = os.getenv("GANDI_SUBDOMAIN")
GANDI_API_KEY = os.getenv("GANDI_API_KEY")

DNS_TTL = os.getenv("DNS_TTL", "300")  # 5 minutes

IP_PROVIDER_URL = os.getenv("IP_PROVIDER_URL", "http://whatismyip.akamai.com/")

def get_ip() -> str:
    """
    find out own IPv4 at home <-- this is the dynamic IP which changes more or less frequently
    similar to curl ifconfig.me/ip, see example.config.py for details to ifconfig providers 
    """ 
    r = requests.get(IP_PROVIDER_URL)
    ip = r.text.strip("\n")
    print(f"Checking dynamic IP with {IP_PROVIDER_URL}: {ip}")
    return ip

def update_ip(gandi_domain, gandi_subdomain, gandi_api_key):
    """
    update IP for the subdomain and domain provided
    curl -X PUT \
        -H "Content-Type: application/json" \
        -H "Authorization: Apikey ${GANDI_API_KEY}" \
        -d "{\"rrset_ttl\": ${DNS_TTL}, \"rrset_values\": [\"<ip>\"]}" \
        https://api.gandi.net/v5/livedns/domains/${GANDI_DOMAIN}/records/${GANDI_SUBDOMAIN}/A
    """
    ip = get_ip()

    url = f"https://api.gandi.net/v5/livedns/domains/{gandi_domain}/records/{gandi_subdomain}/A"
    headers = {"Content-Type": "application/json", "Authorization": f"Apikey {gandi_api_key}"}
    payload = {"rrset_ttl": int(DNS_TTL), "rrset_values": [ip]}

    r = requests.put(
        url=url,
        json=payload,
        headers=headers
    )

    if r.status_code != 201:
        print(f"Status Code is {r.status_code} instead of 201, something went wrong : {r.text}")
        exit(1)
    
    r = requests.get(url=url, headers=headers)
    r.raise_for_status()
    r_json = r.json()
    print(f"The current A records for {gandi_subdomain}.{gandi_domain} is {r_json['rrset_values']}")


if __name__ == "__main__":
    update_ip(GANDI_DOMAIN, GANDI_SUBDOMAIN, GANDI_API_KEY)
