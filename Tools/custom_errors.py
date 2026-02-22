class RUSureThatThisIsPossible(Exception):
    def __init__(self,message):
        super().__init__(message)

class UserExistsException(Exception):
    def __init__(self,message):
        super().__init__(message)

class UserDoesNotExistException(Exception):
    def __init__(self,message):
        super().__init__(message)

class PasswordDoesNotMatchException(Exception):
    def __init__(self,message):
        super().__init__(message)

class PasswordMatchException(Exception):
    def __init__(self,message):
        super().__init__(message)

class UserNameMatchException(Exception):
    def __init__(self,message):
        super().__init__(message)

class UserNameDoesNotMatchException(Exception):
    def __init__(self,message):
        super().__init__(message)