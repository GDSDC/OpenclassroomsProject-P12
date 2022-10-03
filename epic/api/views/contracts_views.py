import logging
from typing import Any, Dict

from django.http import JsonResponse
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from api.decorators import user_has_role, query_parameter_parser, logging_and_response
from api.serializers import ContractSerializer
from core.users.models import User
from core.contacts.models import Contact
from core.contacts.services import contact_exists
from core.contracts.models import Contract
from core.contracts.services import contract_exists


class GlobalContractView(APIView):
    """Global Contract View for creating a contract or get list of contracts."""

    permission_classes = (IsAuthenticated,)
    serializer_class = ContractSerializer

    @query_parameter_parser(
        {'client_id', 'sales_id', 'status',
         'amount_lower', 'amount_upper',
         'payment_due_lower', 'payment_due_upper'})
    def get(self, request, query_params: Dict[str, Any] = {}):
        contracts = Contract.objects.filter(**query_params)
        return JsonResponse(self.serializer_class(contracts, many=True).data, status=status.HTTP_200_OK, safe=False)

    @user_has_role({User.Role.ADMIN, User.Role.SALES})
    def post(self, request, contact_id):
        logger = logging.getLogger('.'.join([__name__, self.__class__.__name__, self.post.__name__]))

        # check if contact exists
        if not contact_exists(contact_id):
            return logging_and_response(
                logger=logger,
                error_message=f"Contact '{contact_id}' not found. Wrong contact_id.",
                error_status=status.HTTP_404_NOT_FOUND)

        contract_to_create = request.data
        contact = Contact.objects.get(id=contact_id)

        # check if user is owner of contact (ie is sales of the contact)
        user = request.user
        if user.role == User.Role.SALES and not contact.sales_id == user.id:
            logger.warning(
                f"Access forbidden ! User '{user.email}' is not attached to contact '{contact_id}' "
                f"({contract_to_create.first_name} {contract_to_create.last_name} "
                f"from {contract_to_create.company_name} company) or admin.")
            return Response('Access forbidden ! You are not attached to the contact or admin.',
                            status=status.HTTP_403_FORBIDDEN)

        serializer = self.serializer_class(data=contract_to_create, context={'contact_id': contact_id}, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return JsonResponse(serializer.data, status=status.HTTP_201_CREATED, safe=False)


class ContractView(APIView):
    """Contract View to interact with a single contract"""

    permission_classes = (IsAuthenticated,)
    serializer_class = ContractSerializer

    def get(self, request, contact_id, contract_id):
        logger = logging.getLogger('.'.join([__name__, self.__class__.__name__, self.get.__name__]))

        # check if contact exists
        if not contact_exists(contact_id):
            return logging_and_response(
                logger=logger,
                error_message=f"Contact '{contact_id}' not found. Wrong contact_id.",
                error_status=status.HTTP_404_NOT_FOUND)

        # check if contract exists
        if not contract_exists(contract_id):
            return logging_and_response(
                logger=logger,
                error_message=f"Contract '{contract_id}' not found. Wrong contract_id.",
                error_status=status.HTTP_404_NOT_FOUND)

        contract = Contract.objects.get(id=contract_id)

        # check if contract belongs to contact
        if not contract.client.id == contact_id:
            return logging_and_response(
                logger=logger,
                error_message=f"Contract '{contract_id}' does not belong to Client '{contact_id}' !",
                error_status=status.HTTP_400_BAD_REQUEST)

        return JsonResponse(self.serializer_class(contract).data, status=status.HTTP_200_OK, safe=False)

    @user_has_role({User.Role.ADMIN, User.Role.SALES})
    def put(self, request, contact_id, contract_id):
        logger = logging.getLogger('.'.join([__name__, self.__class__.__name__, self.put.__name__]))

        # check if contact exists
        if not contact_exists(contact_id):
            return logging_and_response(
                logger=logger,
                error_message=f"Contact '{contact_id}' not found. Wrong contact_id.",
                error_status=status.HTTP_404_NOT_FOUND)

        # check if contract exists
        if not contract_exists(contract_id):
            return logging_and_response(
                logger=logger,
                error_message=f"Contract '{contract_id}' not found. Wrong contract_id.",
                error_status=status.HTTP_404_NOT_FOUND)

        contract_updated_data = request.data
        contract_to_update = Contract.objects.get(id=contract_id)

        # check if contract belongs to contact
        if not contract_to_update.client_id == contact_id:
            return logging_and_response(
                logger=logger,
                error_message=f"Contract '{contract_id}' does not belong to Client '{contact_id}' !",
                error_status=status.HTTP_400_BAD_REQUEST)

        # check if user is owner of contact (ie is sales of the contact)
        user = request.user
        contact = Contact.objects.get(id=contact_id)
        if user.role == User.Role.SALES and not contact.sales_id == user.id:
            logger.warning(
                f"Access forbidden ! User '{user.email}' is not attached to contact '{contact_id}' "
                f"({contact_to_update.first_name} {contact_to_update.last_name} "
                f"from {contact_to_update.company_name} company) or admin.")
            return Response('Access forbidden ! You are not attached to the contact or admin.',
                            status=status.HTTP_403_FORBIDDEN)

        serializer = self.serializer_class(contract_to_update, data=contract_updated_data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return JsonResponse(serializer.data, status=status.HTTP_200_OK)

    @user_has_role({User.Role.ADMIN})
    def delete(self, request, contact_id, contract_id):
        logger = logging.getLogger('.'.join([__name__, self.__class__.__name__, self.delete.__name__]))

        # check if contact exists
        if not contact_exists(contact_id):
            return logging_and_response(
                logger=logger,
                error_message=f"Contact '{contact_id}' not found. Wrong contact_id.",
                error_status=status.HTTP_404_NOT_FOUND)

        # check if contract exists
        if not contract_exists(contract_id):
            return logging_and_response(
                logger=logger,
                error_message=f"Contract '{contract_id}' not found. Wrong contract_id.",
                error_status=status.HTTP_404_NOT_FOUND)

        contract_to_delete = Contract.objects.get(id=contract_id)

        # check if contract belongs to contact
        if not contract_to_delete.client_id == contact_id:
            return logging_and_response(
                logger=logger,
                error_message=f"Contract '{contract_id}' does not belong to Client '{contact_id}' !",
                error_status=status.HTTP_400_BAD_REQUEST)

        contract_to_delete.delete()
        return Response('Contract deleted successfully !', status=status.HTTP_200_OK)
