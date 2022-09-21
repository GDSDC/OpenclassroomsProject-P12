from rest_framework import status
from typing import Tuple, Optional

from core.users.models import User
from core.users.services import user_exists






# ----------- GETTING USER BY ID ------------------

def get_user(user_id: int) -> Tuple[Optional[User], Optional[str], Optional[int]]:
    """Function to get a user if it exists"""

    if not user_exists(user_id=user_id):
        result = (None,
                  RESPONSES['user_not_found']['message'],
                  RESPONSES['user_not_found']['status'])
    else:
        user = User.objects.get(id=user_id)
        result = (user, None, None)

    return result