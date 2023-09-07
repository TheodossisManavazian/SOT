from pydantic import BaseModel
from typing import List


class AddDeleteTickersRequest(BaseModel):
    symbols: List[str]
