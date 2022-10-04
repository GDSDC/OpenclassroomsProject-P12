from datetime import datetime
import logging
from functools import wraps
from typing import Set, Dict

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
                logger = logging.getLogger('.'.join([__name__, user_has_role.__name__]))
                logger.warning(f'Access forbidden ! User {user.email} is not allowed. '
                               f'User need to be {" or ".join([role for role in roles_in])}.')
                return Response(data='Access forbidden ! You are not allowed to do this. ',
                                status=status.HTTP_403_FORBIDDEN)
            else:
                return f(*args, **kwargs)

        return wrapper

    return _inner


# -------- Query Parameters Decorators --------

def query_parameter_parser_backup(validated_query_params: Set[str]):
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
                    return logging_and_response(
                        logger=logging.getLogger('.'.join([__name__, query_parameter_parser_backup.__name__, 'main'])),
                        error_message=f"Query parameter Key Error! Query parameters keys must be "
                                      f"{' and/or '.join([qp for qp in validated_query_params])}.",
                        error_status=status.HTTP_400_BAD_REQUEST)

            # CLIENT_ID /// check for 'client_id' proper query parameter
            client_id_qp = query_params.get('client_id', None)
            if client_id_qp is not None:
                # check for 'client' query parameter proper type -> int
                try:
                    client_id_qp = int(client_id_qp)
                    # check if client exists
                    if not contact_exists(client_id_qp):
                        return logging_and_response(
                            logger=logging.getLogger(
                                '.'.join([__name__, query_parameter_parser_backup.__name__, 'client_id'])),
                            error_message=f'Client "{client_id_qp}" not found !',
                            error_status=status.HTTP_404_NOT_FOUND)
                    query_params_arg['client_id'] = client_id_qp
                except ValueError:
                    return logging_and_response(
                        logger=logging.getLogger(
                            '.'.join([__name__, query_parameter_parser_backup.__name__, 'client_id'])),
                        error_message="'client_id' query parameter wrong value. 'client_id' must be an integer !",
                        error_status=status.HTTP_400_BAD_REQUEST)

            # SALES_ID /// check for 'sales_id' proper query parameter
            sales_id_qp = query_params.get('sales_id', None)
            if sales_id_qp is not None:
                # check for 'sales' query parameter proper type -> int or null
                try:
                    sales_id_qp = int(sales_id_qp)
                    # check if user exists
                    if not user_exists(sales_id_qp):
                        return logging_and_response(
                            logger=logging.getLogger(
                                '.'.join([__name__, query_parameter_parser_backup.__name__, 'sales_id'])),
                            error_message=f'Sales {sales_id_qp} not found !',
                            error_status=status.HTTP_404_NOT_FOUND)
                    query_params_arg['sales_id'] = sales_id_qp
                except ValueError:
                    if sales_id_qp == 'null':
                        query_params_arg['sales_id'] = None
                    else:
                        return logging_and_response(
                            logger=logging.getLogger(
                                '.'.join([__name__, query_parameter_parser_backup.__name__, 'sales_id'])),
                            error_message="'sales_id' query parameter wrong value. "
                                          "'sales_id' must be an integer or null!",
                            error_status=status.HTTP_400_BAD_REQUEST)

            # COMPANY_NAME /// check for contact proper company_name query parameter
            company_name_qp = query_params.get('company_name', None)
            if company_name_qp is not None:
                query_params_arg['company_name__icontains'] = company_name_qp

            # EMAIL /// check for contact proper email query parameter
            email_qp = query_params.get('email', None)
            if email_qp is not None:
                query_params_arg['email__icontains'] = email_qp

            # IS_CLIENT /// check for 'is_client' proper query parameter
            is_client_qp = query_params.get('is_client', None)
            if is_client_qp is not None:
                # check for 'is_client' query parameter proper type -> bool
                if not (is_client_qp == 'true' or is_client_qp == 'false'):
                    return logging_and_response(
                        logger=logging.getLogger(
                            '.'.join([__name__, query_parameter_parser_backup.__name__, 'is_client'])),
                        error_message="'is_client' query parameter wrong value. "
                                      "'is_client' must be 'true' or 'false' !",
                        error_status=status.HTTP_400_BAD_REQUEST)
                query_params_arg['is_client'] = True if is_client_qp == 'true' else False

            # STATUS // check for status proper query parameter
            status_qp = query_params.get('status', None)
            if status_qp is not None:
                # check for 'status' query parameter proper type -> bool
                if not (status_qp == 'true' or status_qp == 'false'):
                    return logging_and_response(
                        logger=logging.getLogger(
                            '.'.join([__name__, query_parameter_parser_backup.__name__, 'status'])),
                        error_message="'status' query parameter wrong value. 'status' must be 'true' or 'false' !",
                        error_status=status.HTTP_400_BAD_REQUEST)
                query_params_arg['status'] = True if status_qp == 'true' else False

            # EVENT_DATE_AFTER // check for 'event_date_after' proper query parameter
            event_date_after_qp = query_params.get('event_date_after', None)
            if event_date_after_qp is not None:
                # check for 'event_date_after' proper type -> isoformat string
                try:
                    event_date_after_qp = datetime.fromisoformat(event_date_after_qp)
                    query_params_arg['event_date__gte'] = make_aware(event_date_after_qp)
                except ValueError:
                    return logging_and_response(
                        logger=logging.getLogger(
                            '.'.join([__name__, query_parameter_parser_backup.__name__, 'event_date_after'])),
                        error_message="'event_date_after' query parameter wrong format! "
                                      "'event_date_after' must be an isoformat string (ex : '2022-09-21').",
                        error_status=status.HTTP_400_BAD_REQUEST)

            # EVENT_DATE_BEFORE // check for 'event_date_before' proper query parameter
            event_date_before_qp = query_params.get('event_date_before', None)
            if event_date_before_qp is not None:
                # check for 'event_date_before' proper type -> isoformat string
                try:
                    event_date_before_qp = datetime.fromisoformat(event_date_before_qp)
                    query_params_arg['event_date__lte'] = make_aware(event_date_before_qp)
                except ValueError:
                    return logging_and_response(
                        logger=logging.getLogger(
                            '.'.join([__name__, query_parameter_parser_backup.__name__, 'event_date_before'])),
                        error_message="'event_date_before' query parameter wrong format! "
                                      "'event_date_before' must be an isoformat string (ex : '2022-09-21').",
                        error_status=status.HTTP_400_BAD_REQUEST)

            # PAYMENT_DUE_AFTER // check for 'payment_due_after' proper query parameter
            payment_due_after_qp = query_params.get('payment_due_after', None)
            if payment_due_after_qp is not None:
                # check for 'payment_due_after' proper type -> isoformat string
                try:
                    payment_due_after_qp = datetime.fromisoformat(payment_due_after_qp)
                    query_params_arg['payment_due__gte'] = make_aware(payment_due_after_qp)
                except ValueError:
                    return logging_and_response(
                        logger=logging.getLogger(
                            '.'.join([__name__, query_parameter_parser_backup.__name__, 'payment_due_after'])),
                        error_message="'payment_due_after' query parameter wrong format! "
                                      "'payment_due_after' must be an isoformat string (ex : '2022-09-21').",
                        error_status=status.HTTP_400_BAD_REQUEST)

            # PAYMENT_DUE_BEFORE // check for 'payment_due_before' proper query parameter
            payment_due_before_qp = query_params.get('payment_due_before', None)
            if payment_due_before_qp is not None:
                # check for 'payment_due_before' proper type -> isoformat string
                try:
                    payment_due_before_qp = datetime.fromisoformat(payment_due_before_qp)
                    query_params_arg['payment_due__lte'] = make_aware(payment_due_before_qp)
                except ValueError:
                    return logging_and_response(
                        logger=logging.getLogger(
                            '.'.join([__name__, query_parameter_parser_backup.__name__, 'payment_due_before'])),
                        error_message="'payment_due_before' query parameter wrong format! "
                                      "'payment_due_before' must be an isoformat string (ex : '2022-09-21').",
                        error_status=status.HTTP_400_BAD_REQUEST)

            # ATTENDEES_ABOVE // check for 'attendees_above' proper query parameter
            attendees_above_qp = query_params.get('attendees_above', None)
            if attendees_above_qp is not None:
                # check for 'attendees_above' proper type -> int
                try:
                    attendees_above_qp = int(attendees_above_qp)
                    query_params_arg['attendees__gte'] = attendees_above_qp
                except ValueError:
                    return logging_and_response(
                        logger=logging.getLogger(
                            '.'.join([__name__, query_parameter_parser_backup.__name__, 'attendees_above'])),
                        error_message="'attendees_above' query parameter wrong format! "
                                      "'attendees_above' must be an integer.",
                        error_status=status.HTTP_400_BAD_REQUEST)

            # ATTENDEES_BELOW // check for 'attendees_below' proper query parameter
            attendees_below_qp = query_params.get('attendees_below', None)
            if attendees_below_qp is not None:
                # check for 'attendees_below' proper type -> int
                try:
                    attendees_below_qp = int(attendees_below_qp)
                    query_params_arg['attendees__lte'] = attendees_below_qp
                except ValueError:
                    return logging_and_response(
                        logger=logging.getLogger(
                            '.'.join([__name__, query_parameter_parser_backup.__name__, 'attendees_below'])),
                        error_message="'attendees_below' query parameter wrong format! "
                                      "'attendees_below' must be an integer.",
                        error_status=status.HTTP_400_BAD_REQUEST)

            # AMOUNT_ABOVE // check for 'amount_above' proper query parameter
            amount_above_qp = query_params.get('amount_above', None)
            if amount_above_qp is not None:
                # check for 'amount_above' proper type -> int
                try:
                    amount_above_qp = int(amount_above_qp)
                    query_params_arg['amount__gte'] = amount_above_qp
                except ValueError:
                    return logging_and_response(
                        logger=logging.getLogger(
                            '.'.join([__name__, query_parameter_parser_backup.__name__, 'amount_above'])),
                        error_message="'amount_above' query parameter wrong format! "
                                      "'amount_above' must be an integer.",
                        error_status=status.HTTP_400_BAD_REQUEST)

            # AMOUNT_BELOW  // check for 'amount_below' proper query parameter
            amount_below_qp = query_params.get('amount_below', None)
            if amount_below_qp is not None:
                # check for 'amount_below' proper type -> int
                try:
                    amount_below_qp = int(amount_below_qp)
                    query_params_arg['amount__lte'] = amount_below_qp
                except ValueError:
                    return logging_and_response(
                        logger=logging.getLogger(
                            '.'.join([__name__, query_parameter_parser_backup.__name__, 'amount_below'])),
                        error_message="'amount_below' query parameter wrong format! "
                                      "'amount_below' must be an integer.",
                        error_status=status.HTTP_400_BAD_REQUEST)

            return f(*args, **kwargs, query_params=query_params_arg)

        return wrapper

    return _inner

# TODO : deploy this decorator and add business responsabilty to views
def query_parameter_parser(query_params_format: Dict[str, type]):
    def _inner(f):
        @wraps(f)
        def wrapper(*args, **kwargs):

            # query parameters checking
            request = args[1]
            query_params = request.query_params
            for qp in query_params:
                # checking valid keys
                if qp not in query_params_format.keys():
                    return logging_and_response(
                        logger=logging.getLogger('.'.join([__name__, query_parameter_parser.__name__])),
                        error_message=f"Query parameter Key Error! Query parameters keys must be "
                                      f"{' and/or '.join([qp for qp in query_params_format.keys()])}.",
                        error_status=status.HTTP_400_BAD_REQUEST)

            # parsing query parameters
            query_params_arg = {}
            error_messages = []
            for qp_key, qp_arg in query_params.items():
                parsed_qp_arg = _pars_arg(qp_arg, query_params_format[qp_key])
                if parsed_qp_arg is not None:
                    query_params_arg[qp_key] = parsed_qp_arg
                elif query_params_format[qp_key] == datetime:
                    error_messages.append(
                        f"'{qp_key}' ValueError ! "
                        f"'{qp_key}' query parameter type must be 'isoformat'.")
                else:
                    error_messages.append(
                        f"'{qp_key}' ValueError ! "
                        f"'{qp_key}' query parameter type must be '{query_params_format[qp_key].__name__}'.")

            if error_messages is not None:
                return logging_and_response(
                    logger=logging.getLogger('.'.join([__name__, query_parameter_parser.__name__])),
                    error_message=' / '.join(error_messages),
                    error_status=status.HTTP_400_BAD_REQUEST)

            return f(*args, **kwargs, query_params=query_params_arg)

        return wrapper

    return _inner


def _pars_arg(arg, cls):
    if cls == str:
        return arg
    if cls == bool:
        return True if arg.lower() == 'true' else False if arg.lower() == 'false' else None
    if cls == datetime:
        try:
            return make_aware(datetime.fromisoformat(arg))
        except ValueError:
            return None
    if cls == int:
        try:
            return int(arg)
        except ValueError:
            return None
    if cls == float:
        try:
            return float(arg)
        except ValueError:
            return None

    return None


def logging_and_response(logger, error_message, error_status):
    logger.warning(error_message)
    return Response(data=error_message, status=error_status)
