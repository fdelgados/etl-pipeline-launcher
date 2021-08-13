import jwt
import datetime

from shared.infrastructure.application.settings import Settings

from identityaccess.domain.service.token_generator import TokenGenerator
from identityaccess.domain.model.user import UserDescriptor


class JwtTokenAuthentication(TokenGenerator):
    _EXPIRATION_TIME_IN_HOURS = 6

    TOKEN_TYPE = 'Bearer'

    def generate(self, user: UserDescriptor) -> str:
        current_time = datetime.datetime.utcnow()

        payload = {
            'sub': user.tenant_id.value,
            'username': user.username,
            'role': user.role,
            'iat': current_time,
            'exp': current_time + datetime.timedelta(hours=self._EXPIRATION_TIME_IN_HOURS)
        }

        token = jwt.encode(payload, Settings.secret_key(), algorithm='HS256')

        return token.decode('utf-8')
