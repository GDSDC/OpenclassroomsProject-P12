from functools import wraps
from typing import Set

from rest_framework import status
from rest_framework.response import Response

from core.users.models import User
from core.users.services import user_exists


# -------- Permissions Decorators --------
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


# -------- Query Parameters Decorators --------

def contact_query_parameter_decorator():
    def _inner(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            request = args[1]
            # query parameters checking
            query_params = request.query_params
            query_params_arg = {}
            # check for validated query parameters
            validated_query_params = ['sales_id', 'company_name', 'is_client']
            for qp in query_params:
                # checking valid keys
                if qp not in validated_query_params:
                    return Response(
                        f"Query parameter Key Error! Query parameters keys must be "
                        f"{' and/or '.join([qp for qp in validated_query_params])}.",
                        status=status.HTTP_400_BAD_REQUEST)

            # check for sales proper query parameter
            sales_id_qp = query_params.get('sales_id', None)
            if sales_id_qp is not None:
                # check for 'sales' query parameter proper type -> int or null
                try:
                    sales_id_qp = int(sales_id_qp)
                    # check if user exists
                    if not user_exists(sales_id_qp):
                        return Response('Sales not found !', status=status.HTTP_404_NOT_FOUND)
                    query_params_arg['sales_id'] = sales_id_qp
                except:
                    if sales_id_qp == 'null':
                        query_params_arg['sales_id'] = None
                    else:
                        return Response("'sales' query parameter wrong value. 'is_client' must be an integer !",
                                        status=status.HTTP_400_BAD_REQUEST)

            # check for contact proper company_name query parameter
            company_name_qp = query_params.get('company_name', None)
            if company_name_qp is not None:
                query_params_arg['company_name'] = company_name_qp


            # check for client proper query parameter
            is_client_qp = query_params.get('is_client', None)
            if is_client_qp is not None:
                # check for 'is_client' query parameter proper type -> bool
                if not (is_client_qp == 'true' or is_client_qp == 'false'):
                    return Response("'is_client' query parameter wrong value. 'is_client' must be 'true' or 'false' !",
                                    status=status.HTTP_400_BAD_REQUEST)
                query_params_arg['is_client'] = True if is_client_qp == 'true' else False

            return f(*args, **kwargs, query_params=query_params_arg)

        return wrapper

    return _inner
