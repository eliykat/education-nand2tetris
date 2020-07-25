class TokenTypeError(Exception):
    """Exception if an illegal token is encountered"""
    def __init__(self, expected, received, token, lineNo):
        self.expected = expected
        self.received = received
        self.token = token
        self.lineNo = lineNo