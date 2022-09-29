from functools import wraps
from typing import Set

from rest_framework import status
from rest_framework.response import Response

from core.contacts.services import contact_exists
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

def query_parameter_decorator(validated_query_params: Set[str]):
    def _inner(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            request = args[1]
            # query parameters checking
            query_params = request.query_params
            query_params_arg = {}
            # check for validated query parameters
            for qp in query_params:
                # checking valid keys
                if qp not in validated_query_params:
                    return Response(
                        f"Query parameter Key Error! Query parameters keys must be "
                        f"{' and/or '.join([qp for qp in validated_query_params])}.",
                        status=status.HTTP_400_BAD_REQUEST)

            # CLIENT_ID /// check for client proper query parameter
            client_id_qp = query_params.get('client_id', None)
            if client_id_qp is not None:
                # check for 'client' query parameter proper type -> int
                try:
                    client_id_qp = int(client_id_qp)
                    # check if client exists
                    if not contact_exists(client_id_qp):
                        return Response('Client not found !', status=status.HTTP_404_NOT_FOUND)
                    query_params_arg['client_id'] = client_id_qp
                except ValueError:
                    return Response(
                        "'client_id' query parameter wrong value. 'client_id' must be an integer !",
                        status=status.HTTP_400_BAD_REQUEST)

            # SALES_ID /// check for sales proper query parameter
            sales_id_qp = query_params.get('sales_id', None)
            if sales_id_qp is not None:
                # check for 'sales' query parameter proper type -> int or null
                try:
                    sales_id_qp = int(sales_id_qp)
                    # check if user exists
                    if not user_exists(sales_id_qp):
                        return Response('Sales not found !', status=status.HTTP_404_NOT_FOUND)
                    query_params_arg['sales_id'] = sales_id_qp
                except ValueError:
                    if sales_id_qp == 'null':
                        query_params_arg['sales_id'] = None
                    else:
                        return Response(
                            "'sales_id' query parameter wrong value. 'sales_id' must be an integer or null!",
                            status=status.HTTP_400_BAD_REQUEST)

            # COMPANY_NAME /// check for contact proper company_name query parameter
            company_name_qp = query_params.get('company_name', None)
            if company_name_qp is not None:
                query_params_arg['company_name__istartswith'] = company_name_qp

            # IS_CLIENT /// check for client proper query parameter
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
