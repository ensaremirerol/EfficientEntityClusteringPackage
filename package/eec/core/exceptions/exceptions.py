class ArgumentException(Exception):
    """Exception thrown when there is a problem with the arguments passed to a function"""

    def __init__(self, message):
        super().__init__(message)


class NotFoundException(Exception):
    """Exception thrown when something is not found"""

    def __init__(self, message):
        super().__init__(message)


class AlreadyExistsException(Exception):
    """Exception thrown when something already exists"""

    def __init__(self, message):
        super().__init__(message)


class AlreadyInClusterException(AlreadyExistsException):
    """Exception thrown when an entity is already in a cluster"""

    def __init__(self, message):
        super().__init__(message)
