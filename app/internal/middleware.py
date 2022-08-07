from fastapi import HTTPException, Header
from internal import enums


def verify_admin(role: str = Header('')):
    if not role or not role == enums.Roles.admin.value:
        raise HTTPException(401)
    return role
