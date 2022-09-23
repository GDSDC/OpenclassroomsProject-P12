from django.http import JsonResponse
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from api.serializers import ContactSerializer
from api.permissions import IsAdmin
from core.users.models import User
from core.contacts.models import Contact


class GlobalContactView(APIView):
    """Contact View"""

    # This view should be accessible only for IsAuthenticated or Authenticated Admin users.
    permission_classes = (IsAuthenticated,)
    serializer_class = ContactSerializer

    # TODO : create decorator to limit access to admin and sales
    def post(self, request):
        contact_to_create = request.data
        serializer = self.serializer_class(data=contact_to_create)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def get(self, request):
        contacts = Contact.objects.all()
        return JsonResponse(self.serializer_class(contacts, many=True).data, status=status.HTTP_200_OK, safe=False)
