from tda import auth

from config import keys

token_path = keys['token_path']
api_key = keys['api_key']
redirect_uri = keys['redirect_uri']

# Handles the connection to the client.
try:
    client = auth.client_from_token_file(token_path, api_key)
except FileNotFoundError:
    from selenium import webdriver

    with webdriver.Chrome(executable_path="/Users/theomanavazian/PycharmProjects/SOT/Externals/chromedriver") as driver:
        client = auth.client_from_login_flow(
            driver, api_key, redirect_uri, token_path)

