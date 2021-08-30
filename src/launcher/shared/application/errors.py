from shared import ApiBaseError, ApiErrorCodes


class InvalidRequestParamsException(ApiBaseError):
    def __init__(self, details: str = "") -> None:
        super().__init__(ApiErrorCodes.INVALID_REQUEST_PARAMETER, details)


class MissingRequestParamsException(ApiBaseError):
    def __init__(self, details: str = "") -> None:
        super().__init__(ApiErrorCodes.MISSING_REQUEST_PARAMETER, details)
