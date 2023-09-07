class InternalServiceException(Exception):
    def __init__(self, msg):
        super(InternalServiceException, self).__init__(msg)


class BadRequestException(Exception):
    def __init__(self, msg):
        super(BadRequestException, self).__init__(msg)


class InvalidTickerException(Exception):
    def __init__(self, msg=None):
        super(InvalidTickerException, self).__init__(f"Invalid Ticker ({msg})")

