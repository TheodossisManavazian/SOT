from typing import Optional
import requests
import config


def _headers() -> dict:
    return {'User-Agent': config.SEC_REQUEST_HEADER_USER_AGENT}


def get_company_facts(cik: str) -> Optional[dict]:
    url = f'https://data.sec.gov/api/xbrl/companyfacts/CIK{cik}.json'
    headers = _headers()
    response = requests.get(url=url, headers=headers)
    if response.status_code == 200:
        return response.json()
    return None

# url_tesla = 'https://data.sec.gov/api/xbrl/companyfacts/CIK0001318605.json'
# url_apple = 'https://data.sec.gov/api/xbrl/companyfacts/CIK0000320193.json'
# url_amd = 'https://data.sec.gov/api/xbrl/companyfacts/CIK0000002488.json'