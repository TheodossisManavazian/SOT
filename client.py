from tda import auth
import config

# Handles the connection to the client.
try:
    client = auth.client_from_token_file(config.TDA_TOKEN_PATH, config.TDA_API_KEY)
except FileNotFoundError:
    from selenium import webdriver

    with webdriver.Chrome(executable_path=config.WEBDRIVER_PATH) as driver:
        client = auth.client_from_login_flow(
            driver, config.TDA_API_KEY, config.TDA_REDIRECT_URI, config.TDA_TOKEN_PATH)

