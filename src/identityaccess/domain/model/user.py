from __future__ import annotations

import abc

from shared_context.domain.model import Repository, AggregateRoot

from identityaccess.domain.model.tenant import TenantId


class UserDescriptor:
    def __init__(self, tenant_id: TenantId, email: str, username: str, role: str):
        self.tenant_id = tenant_id
        self.email = email
        self.username = username
        self.role = role


class User(AggregateRoot):
    def __init__(
        self,
        tenant_id: TenantId,
        username: str,
        password: str,
        email: str,
        role: str
    ):
        self.tenant_id = tenant_id
        self.username = username
        self.password = password
        self.email = email
        self.role = role
        self.is_enabled = False
        self.first_name = None
        self.last_name = None

    def enable(self) -> None:
        self.is_enabled = True

    def user_descriptor(self) -> UserDescriptor:
        return UserDescriptor(
            self.tenant_id,
            self.email,
            self.username,
            self.role
        )


class UserRepository(Repository, metaclass=abc.ABCMeta):
    @classmethod
    def __subclasshook__(cls, subclass):
        if subclass is not UserRepository:
            return NotImplementedError

        if not hasattr(subclass, "user_from_credentials") or not callable(subclass.user_from_credentials):
            return NotImplementedError

    @abc.abstractmethod
    def user_from_credentials(self, tenant_id: TenantId, username: str, password: str) -> User:
        raise NotImplementedError
