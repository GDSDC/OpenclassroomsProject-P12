from datetime import datetime
import logging
from typing import Any, Dict

from django.http import JsonResponse
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework import status

from api.serializers import EventSerializer
from api.decorators import user_has_role, query_parameter_parser
from core.users.models import User
from core.users.services import user_exists
from core.clients.models import Client
from core.clients.services import client_exists
from core.contracts.models import Contract
from core.contracts.services import contract_exists
from core.events.models import Event
from core.events.services import event_exists


class GlobalEventView(APIView):
    """Global Event View for creating an event or get list of events."""

    permission_classes = (IsAuthenticated,)
    serializer_class = EventSerializer

    @query_parameter_parser(
        {'client_id': int, 'support_id': int, 'status': bool, 'client_company_name': str,
         'client_email': str    , 'attendees_above': float, 'attendees_below': float,
         'event_date_after': datetime, 'event_date_before': datetime})
    def get(self, request, query_params: Dict[str, Any]):
        logger = logging.getLogger('.'.join([__name__, self.__class__.__name__, self.get.__name__]))

        # client_id query parameter /// check if client exists
        if 'client_id' in query_params.keys():
            if not client_exists(query_params['client_id']):
                return JsonResponse(data={'detail' : f"Client '{query_params['client_id']}' not found !"},
                                status=status.HTTP_404_NOT_FOUND, safe=False)

        # support_id query parameter /// check if user exists and is Support
        if 'support_id' in query_params.keys() and query_params['support_id'] is not None:
            if not user_exists(query_params['support_id']):
                return JsonResponse(data={'detail' : f"Support '{query_params['support_id']}' not found !"},
                                status=status.HTTP_404_NOT_FOUND, safe=False)
            else:
                # check if 'support_id' correspond to a SUPPORT
                qp_user_role = User.objects.get(id=query_params['support_id']).role
                if qp_user_role != User.Role.SUPPORT:
                    # only log for this part
                    logger.warning(f"User '{query_params['support_id']}' is {qp_user_role}, not SUPPORT !")

        events = Event.objects.filter(**query_params)
        return JsonResponse(self.serializer_class(events, many=True).data, status=status.HTTP_200_OK, safe=False)

    @user_has_role({User.Role.STAFF, User.Role.SALES})
    def post(self, request, client_id):
        logger = logging.getLogger('.'.join([__name__, self.__class__.__name__, self.post.__name__]))

        # check if client exists
        if not client_exists(client_id):
            return JsonResponse(data={'detail' : f"Contact '{client_id}' not found. Wrong client_id."},
                            status=status.HTTP_404_NOT_FOUND, safe=False)

        event_to_create = request.data
        client = Client.objects.get(id=client_id)

        # check if user is owner of client (ie is sales of the client) or if is admin
        user = request.user
        if user.role == User.Role.SALES and not client.sales_id == user.id:
            logger.warning(
                f"Access forbidden ! User '{user.email}' is not attached to client '{client_id}' "
                f"({client.first_name} {client.last_name} "
                f"from {client.company_name} company) or admin.")
            return JsonResponse({'detail' : 'Access forbidden ! You are not attached to the client or admin.'},
                            status=status.HTTP_403_FORBIDDEN, safe=False)

        serializer = self.serializer_class(data=event_to_create, context={'client_id': client_id})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return JsonResponse(serializer.data, status=status.HTTP_201_CREATED, safe=False)


class EventView(APIView):
    """Event view to interact with a single event"""

    permission_classes = (IsAuthenticated,)
    serializer_class = EventSerializer

    def get(self, request, client_id, event_id):
        logger = logging.getLogger('.'.join([__name__, self.__class__.__name__, self.get.__name__]))

        # check if client exists
        if not client_exists(client_id):
            return JsonResponse(data={'detail' : f"Contact '{client_id}' not found. Wrong client_id."},
                            status=status.HTTP_404_NOT_FOUND, safe=False)

        # check if event exists
        if not event_exists(event_id):
            return JsonResponse(data={'detail' : f"Event '{event_id}' not found. Wrong event_id."},
                            status=status.HTTP_404_NOT_FOUND, safe=False)

        event = Event.objects.get(id=event_id)

        # check if event belongs to client
        if not event.client.id == client_id:
            logging.warning(f"Event '{event_id}' does not belong to Client '{client_id}' "
                            f"but Client {event.client_id} !")
            return JsonResponse(data={'detail' : f"Event '{event_id}' does not belong to Client '{client_id}' !"},
                            status=status.HTTP_400_BAD_REQUEST, safe=False)

        return JsonResponse(self.serializer_class(event).data, status=status.HTTP_200_OK, safe=False)

    @user_has_role({User.Role.STAFF, User.Role.SALES, User.Role.SUPPORT})
    def put(self, request, client_id, event_id):
        logger = logging.getLogger('.'.join([__name__, self.__class__.__name__, self.put.__name__]))

        # check if client exists
        if not client_exists(client_id):
            return JsonResponse(data={'detail' : f"Contact '{client_id}' not found. Wrong client_id."},
                            status=status.HTTP_404_NOT_FOUND, safe=False)

        # check if event exists
        if not event_exists(event_id):
            return JsonResponse(data={'detail' : f"Event '{event_id}' not found. Wrong event_id."},
                            status=status.HTTP_404_NOT_FOUND, safe=False)

        event_updated_data = request.data
        event_to_update = Event.objects.get(id=event_id)

        # check if event belongs to client
        if not event_to_update.client.id == client_id:
            logging.warning(f"Event '{event_id}' does not belong to Client '{client_id}' "
                            f"but Client {event_to_update.client_id} !")
            return JsonResponse(data={'detail' : f"Event '{event_id}' does not belong to Client '{client_id}' !"},
                            status=status.HTTP_400_BAD_REQUEST, safe=False)

        # check if user is owner of client (ie is sales of the client)
        user = request.user
        client = Client.objects.get(id=client_id)
        if user.role == User.Role.SALES and not client.sales_id == user.id:
            logger.warning(
                f"Access forbidden ! User '{user.email}' is not attached to client '{client_id}' "
                f"({client.first_name} {client.last_name} "
                f"from {client.company_name} company) or admin.")
            return JsonResponse({'detail' : 'Access forbidden ! You are not attached to the client or ADMIN.'},
                            status=status.HTTP_403_FORBIDDEN, safe=False)

        # check if user is attached to event (ie is support of the event)
        if user.role == User.Role.SUPPORT and not event_to_update.support_id == user.id:
            logger.warning(
                f"Access forbidden ! User '{user.email}' is not attached to event '{event_id}' or ADMIN.")
            return JsonResponse({'detail' : 'Access forbidden ! You are not attached to the event or admin.'},
                            status=status.HTTP_403_FORBIDDEN, safe=False)

        serializer = self.serializer_class(event_to_update, data=event_updated_data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return JsonResponse(serializer.data, status=status.HTTP_200_OK)

    @user_has_role({User.Role.STAFF})
    def delete(self, request, client_id, event_id):
        logger = logging.getLogger('.'.join([__name__, self.__class__.__name__, self.delete.__name__]))

        # check if client exists
        if not client_exists(client_id):
            return JsonResponse(data={'detail' : f"Contact '{client_id}' not found. Wrong client_id."},
                            status=status.HTTP_404_NOT_FOUND, safe=False)

        # check if event exists
        if not event_exists(event_id):
            return JsonResponse(data={'detail' : f"Event '{event_id}' not found. Wrong event_id."},
                            status=status.HTTP_404_NOT_FOUND, safe=False)

        event_to_delete = Event.objects.get(id=event_id)

        # check if event belongs to client
        if not event_to_delete.client.id == client_id:
            logging.warning(f"Event '{event_id}' does not belong to Client '{client_id}' "
                            f"but Client {event_to_delete.client_id} !")
            return JsonResponse(data={'detail' : f"Event '{event_id}' does not belong to Client '{client_id}' !"},
                            status=status.HTTP_400_BAD_REQUEST, safe=False)

        event_to_delete.delete()
        return JsonResponse({'detail' : 'Event deleted successfully !'}, status=status.HTTP_200_OK, safe=False)
