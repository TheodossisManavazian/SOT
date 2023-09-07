import pydash
from sec_cik_mapper import StockMapper

from sot_service.apis.sec_api import get_company_facts
from sot_service.models.sec_company_facts import SECCompanyFacts


def get_sec_company_facts(ticker: str) -> SECCompanyFacts:
    mapper = StockMapper()
    cik = pydash.get(mapper.ticker_to_cik, ticker)
    company_facts = get_company_facts(cik)
    if company_facts:
        return SECCompanyFacts.from_api(company_facts)
