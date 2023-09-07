from typing import Optional, List

from sqlalchemy.engine.cursor import LegacyCursorResult


def single_nullable_result(result) -> Optional[dict]:
    if result is None:
        return None
    else:
        return dict(result)


def list_results(results) -> Optional[List[dict]]:
    return [dict(result) for result in results]
