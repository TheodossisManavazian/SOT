import pydash
from fastapi import Request, Header, HTTPException
from sot_service import engine
from sot_service.daos import auth_dao


def extract_auth_token(header: Header):
    auth_header = pydash.get(header, 'Authorization')
    if auth_header is None:
        return None
    return auth_header.split(" ")[-1]


def requires_auth(request: Request):
    token = extract_auth_token(request.headers)
    if token is None:
        raise HTTPException(
            status_code=401,
            detail="No Auth Token Provided"
        )
    lookup_request = {
        'token': token
    }
    with engine.connect() as conn:
        user_id = auth_dao.lookup_key(conn, lookup_request)
        if user_id is None:
            raise HTTPException(
                status_code=401,
                detail="Unauthorized"
            )
