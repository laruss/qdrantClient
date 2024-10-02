class BaseError(Exception):
    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message)


class NotAuthorizedError(BaseError):
    pass


class NotFoundError(BaseError):
    pass


class ForbiddenError(BaseError):
    pass


class BadRequestError(BaseError):
    pass


class ApplicationError(BaseError):
    pass
