class ReadClientException(Exception):
    "Raised when the client message couldn't be read."
    pass


class SendClientException(Exception):
    "Raised when the message couldn't be send to the client."
    pass
