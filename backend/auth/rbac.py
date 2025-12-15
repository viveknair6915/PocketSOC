from enum import Enum

class Role(str, Enum):
    ADMIN = "admin"
    ANALYST = "analyst"
    AGENT = "agent"

class RBAC:
    role_permissions = {
        Role.ADMIN: ["read_incidents", "delete_incidents", "manage_users"],
        Role.ANALYST: ["read_incidents"],
        Role.AGENT: ["report_incident"]
    }

    @staticmethod
    def check_permission(role: Role, permission: str):
        return permission in RBAC.role_permissions.get(role, [])
