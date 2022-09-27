from functools import wraps
from typing import Set

from rest_framework import status
from rest_framework.response import Response

from core.users.models import User


def user_has_role(roles_in: Set[User.Role]):
    def _inner(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            request = args[1]
            user = request.user
            if user.role not in roles_in:
                return Response('Access forbidden ! You are not allowed to do this.', status=status.HTTP_403_FORBIDDEN)
            else:
                return f(*args, **kwargs)

        return wrapper

    return _inner
