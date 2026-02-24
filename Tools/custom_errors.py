class RUSureThatThisIsPossible(Exception):
    def __init__(self,message):
        super().__init__(message)

class ExistsException(Exception):
    def __init__(self,message):
        super().__init__(message)

class DoesNotExistException(Exception):
    def __init__(self,message):
        super().__init__(message)

class MatchesException(Exception):
    def __init__(self,message):
        super().__init__(message)

class DoesNotMatchException(Exception):
    def __init__(self,message):
        super().__init__(message)