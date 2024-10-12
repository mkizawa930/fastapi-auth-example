class DatabaseError(Exception):
    pass


class AuthenticationError(Exception):
    pass


class PasswordMismatch(AuthenticationError):
    pass


class ResourceNotFound(Exception):
    pass
