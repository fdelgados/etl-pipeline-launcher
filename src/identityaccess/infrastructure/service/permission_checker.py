from identityaccess.domain.model.tenant import TenantId
from identityaccess.domain.model.role import Role
from identityaccess.domain.model.scope import Scope
from identityaccess.domain.service.permission_checker import PermissionChecker, PermissionDeniedError
from identityaccess.domain.model.permission import PermissionRepository

from identityaccess import ErrorCodes


class DbPermissionChecker(PermissionChecker):
    def __init__(self, permission_repository: PermissionRepository):
        self._permission_repository = permission_repository

    def check(self, tenant_id: TenantId, role: Role, scope: Scope) -> None:
        if not self._permission_repository.is_allowed_for(tenant_id, role.name, scope.name):
            raise PermissionDeniedError(
                ErrorCodes.PERMISSION_DENIED,
                details='Access to resource <{}> is not allowed to role <{}>'.format(scope.name, role.name)
            )
