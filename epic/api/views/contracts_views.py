from datetime import datetime
import logging
from typing import Any, Dict

from django.http import JsonResponse
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from api.decorators import user_has_role, query_parameter_parser
from api.serializers import ContractSerializer
from core.users.models import User
from core.users.services import user_exists
from core.clients.models import Client
from core.clients.services import client_exists
from core.contracts.models import Contract
from core.contracts.services import contract_exists


class GlobalContractView(APIView):
    """Global Contract View for creating a contract or get list of contracts."""

    permission_classes = (IsAuthenticated,)
    serializer_class = ContractSerializer

    @query_parameter_parser(
        {'client_id': int, 'sales_id': int, 'status': bool,
         'amount_above': float, 'amount_below': float,
         'payment_due_after': datetime, 'payment_due_before': datetime})
    def get(self, request, query_params: Dict[str, Any]):
        logger = logging.getLogger('.'.join([__name__, self.__class__.__name__, self.get.__name__]))

        # sales_id query parameter /// check if user exists and is Sales
        if 'sales_id' in query_params.keys() and query_params['sales_id'] is not None:
            if not user_exists(query_params['sales_id']):
                return Response(data=f"Sales '{query_params['sales_id']}' not found !",
                                status=status.HTTP_404_NOT_FOUND)
            else:
                # check if 'sales_id' correspond to a SALES
                qp_user_role = User.objects.get(id=query_params['sales_id']).role
                if qp_user_role != User.Role.SALES:
                    # only log for this part
                    logger.warning(f"User '{query_params['sales_id']}' is {qp_user_role}, not SALES !")

        # client_id query parameter /// check if client exists
        if 'client_id' in query_params.keys():
            if not client_exists(query_params['client_id']):
                return Response(data=f"Client '{query_params['client_id']}' not found !",
                                status=status.HTTP_404_NOT_FOUND)

        contracts = Contract.objects.filter(**query_params)
        return JsonResponse(self.serializer_class(contracts, many=True).data, status=status.HTTP_200_OK, safe=False)

    @user_has_role({User.Role.ADMIN, User.Role.SALES})
    def post(self, request, client_id):
        logger = logging.getLogger('.'.join([__name__, self.__class__.__name__, self.post.__name__]))

        # check if client exists
        if not client_exists(client_id):
            return Response(data=f"Contact '{client_id}' not found. Wrong client_id.",
                            status=status.HTTP_404_NOT_FOUND)

        contract_to_create = request.data
        client = Client.objects.get(id=client_id)

        # check if user is owner of client (ie is sales of the client)
        user = request.user
        if user.role == User.Role.SALES and not client.sales_id == user.id:
            logger.warning(
                f"Access forbidden ! User '{user.email}' is not attached to client '{client_id}' "
                f"({contract_to_create.first_name} {contract_to_create.last_name} "
                f"from {contract_to_create.company_name} company) or admin.")
            return Response('Access forbidden ! You are not attached to the client or admin.',
                            status=status.HTTP_403_FORBIDDEN)

        serializer = self.serializer_class(data=contract_to_create, context={'client_id': client_id}, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return JsonResponse(serializer.data, status=status.HTTP_201_CREATED, safe=False)


class ContractView(APIView):
    """Contract View to interact with a single contract"""

    permission_classes = (IsAuthenticated,)
    serializer_class = ContractSerializer

    def get(self, request, client_id, contract_id):
        logger = logging.getLogger('.'.join([__name__, self.__class__.__name__, self.get.__name__]))

        # check if client exists
        if not client_exists(client_id):
            return Response(data=f"Contact '{client_id}' not found. Wrong client_id.",
                            status=status.HTTP_404_NOT_FOUND)

        # check if contract exists
        if not contract_exists(contract_id):
            return Response(data=f"Contract '{contract_id}' not found. Wrong contract_id.",
                            status=status.HTTP_404_NOT_FOUND)

        contract = Contract.objects.get(id=contract_id)

        # check if contract belongs to client
        if not contract.client.id == client_id:
            logger.warning(f"Contract '{contract_id}' does not belong to Client '{client_id}' "
                           f"but Client '{contract.client_id}' !")
            return Response(data=f"Contract '{contract_id}' does not belong to Client '{client_id}' !",
                            status=status.HTTP_400_BAD_REQUEST)

        return JsonResponse(self.serializer_class(contract).data, status=status.HTTP_200_OK, safe=False)

    @user_has_role({User.Role.ADMIN, User.Role.SALES})
    def put(self, request, client_id, contract_id):
        logger = logging.getLogger('.'.join([__name__, self.__class__.__name__, self.put.__name__]))

        # check if client exists
        if not client_exists(client_id):
            return Response(data=f"Contact '{client_id}' not found. Wrong client_id.",
                            status=status.HTTP_404_NOT_FOUND)

        # check if contract exists
        if not contract_exists(contract_id):
            return Response(data=f"Contract '{contract_id}' not found. Wrong contract_id.",
                            status=status.HTTP_404_NOT_FOUND)

        contract_updated_data = request.data
        contract_to_update = Contract.objects.get(id=contract_id)

        # check if contract belongs to client
        if not contract_to_update.client_id == client_id:
            logger.warning(f"Contract '{contract_id}' does not belong to Client '{client_id}' "
                           f"but Client '{contract_to_update.client_id}' !")
            return Response(data=f"Contract '{contract_id}' does not belong to Client '{client_id}' !",
                            status=status.HTTP_400_BAD_REQUEST)

        # check if user is owner of client (ie is sales of the client)
        user = request.user
        client = Client.objects.get(id=client_id)
        if user.role == User.Role.SALES and not client.sales_id == user.id:
            logger.warning(
                f"Access forbidden ! User '{user.email}' is not attached to client '{client_id}' "
                f"({client_to_update.first_name} {client_to_update.last_name} "
                f"from {client_to_update.company_name} company) or admin.")
            return Response('Access forbidden ! You are not attached to the client or admin.',
                            status=status.HTTP_403_FORBIDDEN)

        serializer = self.serializer_class(contract_to_update, data=contract_updated_data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return JsonResponse(serializer.data, status=status.HTTP_200_OK)

    @user_has_role({User.Role.ADMIN})
    def delete(self, request, client_id, contract_id):
        logger = logging.getLogger('.'.join([__name__, self.__class__.__name__, self.delete.__name__]))

        # check if client exists
        if not client_exists(client_id):
            return Response(data=f"Contact '{client_id}' not found. Wrong client_id.",
                            status=status.HTTP_404_NOT_FOUND)

        # check if contract exists
        if not contract_exists(contract_id):
            return Response(data=f"Contract '{contract_id}' not found. Wrong contract_id.",
                            status=status.HTTP_404_NOT_FOUND)

        contract_to_delete = Contract.objects.get(id=contract_id)

        # check if contract belongs to client
        if not contract_to_delete.client_id == client_id:
            logger.warning(f"Contract '{contract_id}' does not belong to Client '{client_id}' "
                           f"but Client '{contract_to_delete.client_id}' !")
            return Response(data=f"Contract '{contract_id}' does not belong to Client '{client_id}' !",
                            status=status.HTTP_400_BAD_REQUEST)

        contract_to_delete.delete()
        return Response('Contract deleted successfully !', status=status.HTTP_200_OK)
