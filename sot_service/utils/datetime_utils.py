import datetime
from typing import Union, Optional

MILLISECONDS = "MILLISECONDS"


def epoch_to_date(epoch: Union[float, str], time_scale: str = MILLISECONDS) -> Optional[datetime.date]:
    if isinstance(epoch, str):
        try:
            epoch = float(epoch)
        except ValueError:
            raise ValueError("Epoch cannot be converted to a float")

    if time_scale == MILLISECONDS:
        return datetime.date.fromtimestamp(epoch / 1000)


def days_between_dates(day1: datetime.date, day2: datetime.date) -> int:
    return (day1 - day2).days
