from datetime import datetime
import logging
from functools import wraps
from typing import Set, Dict

from django.utils.timezone import make_aware
from rest_framework import status
from rest_framework.response import Response

from core.clients.services import client_exists
from core.users.models import User
from core.users.services import user_exists

# Query Parameters Filters
QP_FILTERS = {
    'client_id': 'client_id',
    'sales_id': 'sales_id',
    'support_id': 'support_id',
    'role': 'role',
    'company_name': 'company_name__icontains',
    'email': 'email__icontains',
    'is_client': 'is_client',
    'status': 'status',
    'event_date_after': 'event_date__gte',
    'event_date_before': 'event_date__lte',
    'payment_due_after': 'payment_due__gte',
    'payment_due_before': 'payment_due__lte',
    'attendees_above': 'attendees__gte',
    'attendees_below': 'attendees__lte',
    'amount_above': 'amount__gte',
    'amount_below': 'amount__lte',
}


# -------- Permissions Decorators --------
def user_has_role(roles_in: Set[User.Role]):
    logger = logging.getLogger('.'.join([__name__, user_has_role.__name__]))

    def _inner(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            request = args[1]
            user = request.user
            if user.role not in roles_in:
                logger.warning(f'Access forbidden ! User {user.email} is not allowed. '
                               f'User need to be {" or ".join([role for role in roles_in])}.')
                return Response(data='Access forbidden ! You are not allowed to do this. ',
                                status=status.HTTP_403_FORBIDDEN)
            else:
                return f(*args, **kwargs)

        return wrapper

    return _inner


# -------- Query Parameters Decorators --------

def query_parameter_parser(query_params_format: Dict[str, type]):
    logger = logging.getLogger('.'.join([__name__, query_parameter_parser.__name__]))

    def _inner(f):
        @wraps(f)
        def wrapper(*args, **kwargs):

            # query parameters checking
            request = args[1]
            query_params = request.query_params
            for qp in query_params:
                # checking valid keys
                if qp not in query_params_format.keys():
                    error_message = f"Query parameter Key Error! Query parameters keys must be " \
                                    f"{' and/or '.join([qp for qp in query_params_format.keys()])}."
                    logger.warning(error_message)
                    return Response(data=error_message,
                                    status=status.HTTP_400_BAD_REQUEST)

            # parsing query parameters
            query_params_arg = {}
            error_messages = []
            for qp_key, qp_arg in query_params.items():
                parsed_qp_arg = _pars_arg(qp_arg, query_params_format[qp_key])
                if parsed_qp_arg is not None:
                    query_params_arg[QP_FILTERS[qp_key]] = parsed_qp_arg
                elif qp_key == 'sales_id' or qp_key == 'support_id':
                    if qp_arg == 'null':
                        query_params_arg[QP_FILTERS[qp_key]] = None
                    else:
                        error_messages.append(
                            f"'{qp_key}' ValueError ! "
                            f"'{qp_key}' query parameter type must be 'int' or value must be 'null'.")
                elif query_params_format[qp_key] == datetime:
                    error_messages.append(
                        f"'{qp_key}' ValueError ! "
                        f"'{qp_key}' query parameter type must be 'isoformat'.")
                elif query_params_format[qp_key] == User.Role:
                    error_messages.append(
                        f"'{qp_key}' ValueError ! "
                        f"'{qp_key}' query parameter value must be {' or '.join(query_params_format[qp_key].values)}")
                else:
                    error_messages.append(
                        f"'{qp_key}' ValueError ! "
                        f"'{qp_key}' query parameter type must be '{query_params_format[qp_key].__name__}'.")

            if error_messages:
                error_message = ' / '.join(error_messages)
                logging.warning(error_message)
                return Response(data=error_message,
                                status=status.HTTP_400_BAD_REQUEST)

            return f(*args, **kwargs, query_params=query_params_arg)

        return wrapper

    return _inner


def _pars_arg(arg, cls):
    if cls == str:
        return arg
    elif cls == bool:
        return True if arg.lower() == 'true' else False if arg.lower() == 'false' else None
    elif cls == datetime:
        try:
            return make_aware(datetime.fromisoformat(arg))
        except ValueError:
            return None
    elif cls == float:
        try:
            return float(arg)
        except ValueError:
            return None
    else:  # enables to parse int and User.Role enum
        try:
            return cls(arg)
        except ValueError:
            return None
