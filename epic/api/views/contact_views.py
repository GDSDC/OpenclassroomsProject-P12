from django.http import JsonResponse
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from api.serializers import ContactSerializer
from api.permissions import IsAdmin
from core.users.models import User
from core.contacts.models import Contact
from core.contacts.services import contact_exists


class GlobalContactView(APIView):
    """Global Contact View for creating a contact or get list of clients."""

    permission_classes = (IsAuthenticated,)
    serializer_class = ContactSerializer

    def post(self, request):
        # check if user is admin or sales
        user = request.user
        if user.role != (User.Role.ADMIN or User.Role.SALES):
            return Response('Access forbidden ! You should be at least Sales or Admin.',
                            status=status.HTTP_403_FORBIDDEN)

        contact_to_create = request.data
        serializer = self.serializer_class(data=contact_to_create)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def get(self, request):
        contacts = Contact.objects.all()
        return JsonResponse(self.serializer_class(contacts, many=True).data, status=status.HTTP_200_OK, safe=False)


class ContactView(APIView):
    """Contact View to interact with a single contact"""
    permission_classes = (IsAuthenticated,)
    serializer_class = ContactSerializer

    def get(self, request, contact_id):
        # check if contact exists
        if not contact_exists(contact_id):
            return Response('Contact not found. Wrong contact_id.', status=status.HTTP_404_NOT_FOUND)

        contact = Contact.objects.get(id=contact_id)
        return JsonResponse(self.serializer_class(contact).data, status=status.HTTP_200_OK, safe=False)

    def put(self, request, contact_id):
        # check if contact exists
        if not contact_exists(contact_id):
            return Response('Contact not found. Wrong contact_id.', status=status.HTTP_404_NOT_FOUND)

        contact_updated_data = request.data
        contact_to_update = Contact.objects.get(id=contact_id)

        serializer = self.serializer_class(contact_to_update, data=contact_updated_data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return JsonResponse(serializer.data, status=status.HTTP_200_OK)


