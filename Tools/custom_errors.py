class RUSureThatThisIsPossible(Exception):
    def __init__(self,message):
        super().__init__(message)

class ExistsException(Exception):
    def __init__(self,message):
        super().__init__(message)

class DoesNotExistException(Exception):
    def __init__(self,message):
        super().__init__(message)

class PasswordDoesNotMatchException(Exception):
    def __init__(self,message):
        super().__init__(message)

class PasswordMatchException(Exception):
    def __init__(self,message):
        super().__init__(message)

class NameMatchesException(Exception):
    def __init__(self,message):
        super().__init__(message)

class NameDoesNotMatchException(Exception):
    def __init__(self,message):
        super().__init__(message)