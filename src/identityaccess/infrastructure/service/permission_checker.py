from identityaccess.domain.model.tenant import TenantId
from identityaccess.domain.model.role import Role
from identityaccess.domain.model.scope import Scope


class PermissionDeniedError(RuntimeError):
    pass


class PermissionChecker:
    def __init__(self):
        self.db_service = ""

    def check(self, tenant_id: TenantId, role: Role, scope: Scope) -> None:
        query = """SELECT * FROM tenant_scopes
            WHERE tenant_id = :tenant_id
            AND role = :role
            AND scope = :scope
        """

        self.db_service.split()

        if not False:
            raise PermissionDeniedError(
                "Permission denied for {} to {}".format(role.name, scope.name)
            )

