import logging
from typing import Any, Dict

from django.http import JsonResponse
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from api.serializers import ClientSerializer
from api.decorators import user_has_role, query_parameter_parser
from core.users.models import User
from core.users.services import user_exists
from core.clients.models import Client
from core.clients.services import client_exists


class GlobalClientView(APIView):
    """Global Client View for creating a client or get list of clients."""

    permission_classes = (IsAuthenticated,)
    serializer_class = ClientSerializer

    @query_parameter_parser({'sales_id': int, 'email': str, 'company_name': str, 'is_client': bool})
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

        clients = Client.objects.filter(**query_params)
        return JsonResponse(self.serializer_class(clients, many=True).data, status=status.HTTP_200_OK, safe=False)

    @user_has_role({User.Role.STAFF, User.Role.SALES})
    def post(self, request):
        client_to_create = request.data
        serializer = self.serializer_class(data=client_to_create, context={'user': request.user})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class ClienttView(APIView):
    """Client View to interact with a single client"""
    permission_classes = (IsAuthenticated,)
    serializer_class = ClientSerializer

    def get(self, request, client_id):

        # check if client exists
        if not client_exists(client_id):
            return Response(data=f"Client '{client_id}' not found. Wrong client_id.",
                            status=status.HTTP_404_NOT_FOUND)

        client = Client.objects.get(id=client_id)
        return JsonResponse(self.serializer_class(client).data, status=status.HTTP_200_OK, safe=False)

    @user_has_role({User.Role.STAFF, User.Role.SALES})
    def put(self, request, client_id):
        logger = logging.getLogger('.'.join([__name__, self.__class__.__name__, self.put.__name__]))

        # check if client exists
        if not client_exists(client_id):
            return Response(data=f"Client '{client_id}' not found. Wrong client_id.",
                            status=status.HTTP_404_NOT_FOUND)

        client_updated_data = request.data
        client_to_update = Client.objects.get(id=client_id)

        # check if user is owner of client (ie is sales of the client)
        user = request.user
        if user.role == User.Role.SALES and not client_to_update.sales_id == user.id:
            logger.warning(
                f"Access forbidden ! User '{user.email}' is not attached to client '{client_id}' "
                f"({client_to_update.first_name} {client_to_update.last_name} "
                f"from {client_to_update.company_name} company) or ADMIN.")
            return Response('Access forbidden ! You are not attached to the client or admin.',
                            status=status.HTTP_403_FORBIDDEN)

        serializer = self.serializer_class(client_to_update, data=client_updated_data,
                                           context={'user': request.user}, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return JsonResponse(serializer.data, status=status.HTTP_200_OK)

    @user_has_role({User.Role.STAFF})
    def delete(self, request, client_id):

        # check if client exists
        if not client_exists(client_id):
            return Response(data=f"Client '{client_id}' not found. Wrong client_id.",
                            status=status.HTTP_404_NOT_FOUND)

        client_to_delete = Client.objects.get(id=client_id)
        client_to_delete.delete()
        return JsonResponse('Client deleted successfully !', status=status.HTTP_200_OK, safe=False)
