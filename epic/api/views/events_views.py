from django.http import JsonResponse
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from api.serializers import EventSerializer
from api.decorators import user_has_role
from core.users.models import User
from core.contacts.models import Contact
from core.contacts.services import contact_exists
from core.contracts.models import Contract
from core.contracts.services import contract_exists
from core.events.models import Event
from core.events.services import event_exists


# from core.events.services import event_exists


class GlobalEventView(APIView):
    """Global Event View for creating an event or get list of events."""

    permission_classes = (IsAuthenticated,)
    serializer_class = EventSerializer

    def get(self, request):
        events = Event.objects.all()
        return JsonResponse(self.serializer_class(events, many=True).data, status=status.HTTP_200_OK, safe=False)

    @user_has_role({User.Role.ADMIN, User.Role.SALES})
    def post(self, request, contact_id):
        # check if contact exists
        if not contact_exists(contact_id):
            return Response('Contact not found. Wrong contact_id.', status=status.HTTP_404_NOT_FOUND)

        event_to_create = request.data
        contact = Contact.objects.get(id=contact_id)

        # check if user is owner of contact (ie is sales of the contact) or if is admin
        user = request.user
        if user.role == User.Role.SALES and not contact.sales_id == user.id:
            return Response('Access forbidden ! You are not attached to the contact or admin.',
                            status=status.HTTP_403_FORBIDDEN)

        serializer = self.serializer_class(data=event_to_create, context={'contact_id': contact_id}, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return JsonResponse(serializer.data, status=status.HTTP_201_CREATED, safe=False)


class EventView(APIView):
    """Event view to interact with a single event"""

    permission_classes = (IsAuthenticated,)
    serializer_class = EventSerializer

    def get(self, request, contact_id, event_id):
        # check if contact exists
        if not contact_exists(contact_id):
            return Response('Contact not found. Wrong contact_id.', status=status.HTTP_404_NOT_FOUND)

        # check if event exists
        if not event_exists(event_id):
            return Response('Event not found. Wrong event_id.', status=status.HTTP_404_NOT_FOUND)

        event = Event.objects.get(id=event_id)

        # check if event belongs to contact
        if not event.client.id == contact_id:
            return Response(f"Event '{event_id}' does not belong to Client '{contact_id}' !",
                            status=status.HTTP_400_BAD_REQUEST)

        return JsonResponse(self.serializer_class(event).data, status=status.HTTP_200_OK, safe=False)

    @user_has_role({User.Role.ADMIN, User.Role.SALES})
    def put(self, request, contact_id, event_id):
        # check if contact exists
        if not contact_exists(contact_id):
            return Response('Contact not found. Wrong contact_id.', status=status.HTTP_404_NOT_FOUND)

        # check if event exists
        if not event_exists(event_id):
            return Response('Event not found. Wrong event_id.', status=status.HTTP_404_NOT_FOUND)

        event_updated_data = request.data
        event_to_update = Event.objects.get(id=event_id)

        # check if event belongs to contact
        if not event_to_update.client.id == contact_id:
            return Response(f"Event '{event_id}' does not belong to Client '{contact_id}' !",
                            status=status.HTTP_400_BAD_REQUEST)

        # check if user is owner of contact (ie is sales of the contact)
        user = request.user
        contact = Contact.objects.get(id=contact_id)
        if user.role == User.Role.SALES and not contact.sales_id == user.id:
            return Response('Access forbidden ! You are not attached to the contact or admin.',
                            status=status.HTTP_403_FORBIDDEN)

        serializer = self.serializer_class(event_to_update, data=event_updated_data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return JsonResponse(serializer.data, status=status.HTTP_200_OK)
