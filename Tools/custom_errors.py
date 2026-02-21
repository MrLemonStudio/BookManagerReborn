class RUSureThatThisIsPossible(Exception):
    def __init(self,message):
        super().__init__(message)

class UserExistsException(Exception):
    def __init(self,message):
        super().__init__(message)

class UserDoesNotExistException(Exception):
    def __init(self,message):
        super().__init__(message)

class PasswordDoesNotMatchException(Exception):
    def __init(self,message):
        super().__init__(message)