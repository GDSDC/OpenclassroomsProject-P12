from datetime import datetime
from functools import wraps
from typing import Set

from django.utils.timezone import make_aware
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

            # CLIENT_ID /// check for 'client_id' proper query parameter
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

            # SALES_ID /// check for 'sales_id' proper query parameter
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

            # IS_CLIENT /// check for 'is_client' proper query parameter
            is_client_qp = query_params.get('is_client', None)
            if is_client_qp is not None:
                # check for 'is_client' query parameter proper type -> bool
                if not (is_client_qp == 'true' or is_client_qp == 'false'):
                    return Response("'is_client' query parameter wrong value. 'is_client' must be 'true' or 'false' !",
                                    status=status.HTTP_400_BAD_REQUEST)
                query_params_arg['is_client'] = True if is_client_qp == 'true' else False

            # STATUS // check for status proper query parameter
            status_qp = query_params.get('status', None)
            if status_qp is not None:
                # check for 'status' query parameter proper type -> bool
                if not (status_qp == 'true' or status_qp == 'false'):
                    return Response("'status' query parameter wrong value. 'status' must be 'true' or 'false' !",
                                    status=status.HTTP_400_BAD_REQUEST)
                query_params_arg['status'] = True if status_qp == 'true' else False

            # EVENT_DATE_LOWER // check for 'event_date_lower' proper query parameter
            event_date_lower_qp = query_params.get('event_date_lower', None)
            if event_date_lower_qp is not None:
                # check for 'event_date_lower' proper type -> isoformat string
                try:
                    event_date_lower_qp = datetime.fromisoformat(event_date_lower_qp)
                    query_params_arg['event_date__gte'] = make_aware(event_date_lower_qp)
                except ValueError:
                    return Response(
                        "'event_date_lower' query parameter wrong format! "
                        "'event_date_lower' must be an isoformat string (ex : '2022-09-21').",
                        status=status.HTTP_400_BAD_REQUEST)

            # EVENT_DATE_UPPER // check for 'event_date_upper' proper query parameter
            event_date_upper_qp = query_params.get('event_date_upper', None)
            if event_date_upper_qp is not None:
                # check for 'event_date_upper' proper type -> isoformat string
                try:
                    event_date_upper_qp = datetime.fromisoformat(event_date_upper_qp)
                    query_params_arg['event_date__lte'] = make_aware(event_date_upper_qp)
                except ValueError:
                    return Response(
                        "'event_date_upper' query parameter wrong format! "
                        "'event_date_upper' must be an isoformat string (ex : '2022-09-21').",
                        status=status.HTTP_400_BAD_REQUEST)

            # PAYMENT_DUE_LOWER // check for 'payment_due_lower' proper query parameter
            payment_due_lower_qp = query_params.get('payment_due_lower', None)
            if payment_due_lower_qp is not None:
                # check for 'payment_due_lower' proper type -> isoformat string
                try:
                    payment_due_lower_qp = datetime.fromisoformat(payment_due_lower_qp)
                    query_params_arg['payment_due__gte'] = make_aware(payment_due_lower_qp)
                except ValueError:
                    return Response(
                        "'payment_due_lower' query parameter wrong format! "
                        "'payment_due_lower' must be an isoformat string (ex : '2022-09-21').",
                        status=status.HTTP_400_BAD_REQUEST)

            # PAYMENT_DUE_UPPER // check for 'payment_due_upper' proper query parameter
            payment_due_upper_qp = query_params.get('payment_due_upper', None)
            if payment_due_upper_qp is not None:
                # check for 'payment_due_upper' proper type -> isoformat string
                try:
                    payment_due_upper_qp = datetime.fromisoformat(payment_due_upper_qp)
                    query_params_arg['payment_due__lte'] = make_aware(payment_due_upper_qp)
                except ValueError:
                    return Response(
                        "'payment_due_upper' query parameter wrong format! "
                        "'payment_due_upper' must be an isoformat string (ex : '2022-09-21').",
                        status=status.HTTP_400_BAD_REQUEST)

            # AMOUNT_LOWER // check for 'payment_due_lower' proper query parameter
            amount_lower_qp = query_params.get('amount_lower', None)
            if amount_lower_qp is not None:
                # check for 'amount_lower' proper type -> int
                try:
                    amount_lower_qp = int(amount_lower_qp)
                    query_params_arg['amount__gte'] = amount_lower_qp
                except ValueError:
                    return Response(
                        "'amount_lower' query parameter wrong format! 'amount_lower' must be an integer.",
                        status=status.HTTP_400_BAD_REQUEST)

            # AMOUNT_UPPER // check for 'amount_upper' proper query parameter
            amount_upper_qp = query_params.get('amount_upper', None)
            if amount_upper_qp is not None:
                # check for 'amount_upper' proper type -> int
                try:
                    amount_upper_qp = int(amount_upper_qp)
                    query_params_arg['amount__lte'] = amount_upper_qp
                except ValueError:
                    return Response(
                        "'amount_lower' query parameter wrong format! 'amount_lower' must be an integer.",
                        status=status.HTTP_400_BAD_REQUEST)

            return f(*args, **kwargs, query_params=query_params_arg)

        return wrapper

    return _inner
