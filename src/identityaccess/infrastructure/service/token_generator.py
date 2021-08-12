import jwt

from shared.infrastructure.application.settings import Settings

from identityaccess.domain.service.token_generator import TokenGenerator
from identityaccess.domain.model.user import UserDescriptor


class JwtTokenAuthentication(TokenGenerator):
    TOKEN_TYPE = "Bearer"

    def generate(self, user: UserDescriptor) -> str:
        payload = {
            "sub": user.tenant_id.value,
            "username": user.username,
            "role": user.role
        }

        token = jwt.encode(payload, Settings.secret_key(), algorithm="HS256")

        return token.decode('utf-8')
