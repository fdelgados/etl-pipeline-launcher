class AccessToken:
    _BEARER_TYPE = 'Bearer'
    _VALID_TOKEN_TYPES = [
        _BEARER_TYPE
    ]

    def __init__(self, access_token: str):
        if not access_token:
            raise ValueError('Access token cannot be empty')

        token_type, token = access_token.split()

        self._ensure_is_valid_token_type(token_type)

        self.token_type = token_type
        self.value = token

    def _ensure_is_valid_token_type(self, token_type: str) -> None:
        if token_type not in self._VALID_TOKEN_TYPES:
            raise ValueError('{} is not a valid token type'.format(token_type))

    def is_bearer(self) -> bool:
        return self.token_type == self._BEARER_TYPE

    def __str__(self) -> str:
        return '{} {}'.format(self.token_type, self.value)
