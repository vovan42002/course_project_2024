from db.models import User


def check_role(allowed_roles: list[str], user: User) -> bool:
    if user.is_vendor and "vendor" in allowed_roles:
        return True
    elif user.is_superuser and "admin" in allowed_roles:
        return True
    elif not user.is_superuser and not user.is_vendor and "user" in allowed_roles:
        return True
    return False
