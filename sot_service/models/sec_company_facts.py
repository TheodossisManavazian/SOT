import pydash

from sot_service.models.constants import sec_response_field_names
from sot_service.utils.model_utils import dict_to_model


class SECCompanyFacts:
    assets: dict
    assets_current: dict
    cost_of_revenue: dict
    debt_current: dict
    dividends: dict
    earnings_per_share_basic: dict
    gross_profit: dict
    increase_decrease_in_accrued_liabilities: dict
    liabilities: dict
    net_income_loss: dict
    operating_expenses: dict
    operating_income_loss: dict
    profit_loss: dict
    revenues: dict

    @staticmethod
    def from_api(response: dict) -> 'SECCompanyFacts':
        return dict_to_model({
            "assets": pydash.get(response, sec_response_field_names.ASSETS),
            "assets_current": pydash.get(response, sec_response_field_names.ASSETS_CURRENT),
            "cost_of_revenue": pydash.get(response, sec_response_field_names.COST_OF_REVENUE),
            "debt_current": pydash.get(response, sec_response_field_names.DEBT_CURRENT),
            "dividends": pydash.get(response, sec_response_field_names.DIVIDENDS),
            "earnings_per_share_basic": pydash.get(response, sec_response_field_names.EARNINGS_PER_SHARE_BASIC),
            "gross_profit": pydash.get(response, sec_response_field_names.GROSS_PROFIT),
            "increase_decrease_in_accrued_liabilities": pydash.get(response, sec_response_field_names.INCREASE_DECREASE_IN_ACCRUED_LIABILITIES),
            "liabilities": pydash.get(response, sec_response_field_names.LIABILITIES),
            "net_income_loss": pydash.get(response, sec_response_field_names.NET_INCOME_LOSS),
            "operating_expenses": pydash.get(response, sec_response_field_names.OPERATING_EXPENSES),
            "operating_income_loss": pydash.get(response, sec_response_field_names.OPERATING_INCOME_LOSS),
            "profit_loss": pydash.get(response, sec_response_field_names.PROFIT_LOSS),
            "revenues": pydash.get(response, sec_response_field_names.REVENUES)
        }, SECCompanyFacts)



