from django.http import JsonResponse
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from api.decorators import user_has_role
from api.serializers import ContractSerializer
from core.users.models import User
from core.contacts.models import Contact
from core.contacts.services import contact_exists
from core.contracts.models import Contract


# from core.contracts.services import contract_exists


class GlobalContractsView(APIView):
    """Global Contract View for creating a contract or get list of contracts."""

    permission_classes = (IsAuthenticated,)
    serializer_class = ContractSerializer

    def get(self, request):
        contracts = Contract.objects.all()
        return JsonResponse(self.serializer_class(contracts, many=True).data, status=status.HTTP_200_OK, safe=False)

    @user_has_role(roles_in={User.Role.SALES, User.Role.ADMIN})
    def post(self, request, contact_id):
        # check if contact exists
        if not contact_exists(contact_id):
            return Response('Contact not found. Wrong contact_id.', status=status.HTTP_404_NOT_FOUND)

        contract_to_create = request.data

        # check if user is owner of contact (ie is sales of the contact) or if is admin
        user = request.user
        if user.role == User.Role.SALES and not Contact.objects.get(id=contact_id).sales_id == user.id:
            return Response('Access forbidden ! You are not attached to the contact.',
                            status=status.HTTP_403_FORBIDDEN)

        serializer = self.serializer_class(data=contract_to_create, context={'contact_id': contact_id}, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
