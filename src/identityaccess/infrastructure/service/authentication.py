from identityaccess.domain.service.authentication import AuthenticationService, AuthenticationError
from identityaccess.domain.model.tenant import TenantId, TenantRepository
from identityaccess.domain.model.user import UserRepository, UserDescriptor
from identityaccess.infrastructure.service.encryption import EncryptionService
from identityaccess import ErrorCodes


class DefaultAuthenticationService(AuthenticationService):
    def __init__(
        self,
        tenant_repository: TenantRepository,
        user_repository: UserRepository
    ):
        self._tenant_repository = tenant_repository
        self._user_repository = user_repository

    def authenticate(self, tenant_id: TenantId, username: str, password: str) -> UserDescriptor:
        tenant = self._tenant_repository.tenant_of_id(tenant_id)

        if not tenant:
            raise AuthenticationError(ErrorCodes.TENANT_NOT_FOUND)

        if not tenant.is_active:
            raise AuthenticationError(ErrorCodes.TENANT_ACCOUNT_DEACTIVATED)

        user = self._user_repository.user_from_credentials(
            tenant_id,
            username,
            EncryptionService.sha1_encrypt(password)
        )

        if not user:
            raise AuthenticationError(ErrorCodes.USER_NOT_FOUND)

        if not user.is_enabled:
            raise AuthenticationError(ErrorCodes.USER_DISABLED)

        return user.user_descriptor()
