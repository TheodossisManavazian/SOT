from fastapi import APIRouter

import config
from client import client

router = APIRouter(prefix='')


@router.get("/", )
@router.get('/ping')
def home_page():
    return {"status": "We're up baby!"}


# @router.get("/test")
# def test():
#     return {"message:": client.get_account(config.TDA_ACCOUNT_NUMBER).json()}
