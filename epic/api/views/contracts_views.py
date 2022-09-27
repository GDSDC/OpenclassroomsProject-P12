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
from core.contracts.services import contract_exists


class GlobalContractView(APIView):
    """Global Contract View for creating a contract or get list of contracts."""

    permission_classes = (IsAuthenticated,)
    serializer_class = ContractSerializer

    def get(self, request):
        contracts = Contract.objects.all()
        return JsonResponse(self.serializer_class(contracts, many=True).data, status=status.HTTP_200_OK, safe=False)

    @user_has_role({User.Role.ADMIN, User.Role.SALES})
    def post(self, request, contact_id):
        # check if contact exists
        if not contact_exists(contact_id):
            return Response('Contact not found. Wrong contact_id.', status=status.HTTP_404_NOT_FOUND)

        contract_to_create = request.data
        contact = Contact.objects.get(id=contact_id)

        # check if user is owner of contact (ie is sales of the contact)
        user = request.user
        if user.role == User.Role.SALES and not contact.sales_id == user.id:
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
        # check if contact exists
        if not contact_exists(contact_id):
            return Response('Contact not found. Wrong contact_id.', status=status.HTTP_404_NOT_FOUND)

        # check if contract exists
        if not contract_exists(contract_id):
            return Response('Contract not found. Wrong contract_id.', status=status.HTTP_404_NOT_FOUND)

        contract = Contract.objects.get(id=contract_id)

        # check if contract belongs to contact
        if not contract.client.id == contact_id:
            return Response(f"Contract '{contract_id}' does not belong to Client '{contact_id}' !",
                            status=status.HTTP_400_BAD_REQUEST)

        return JsonResponse(self.serializer_class(contract).data, status=status.HTTP_200_OK, safe=False)

    @user_has_role({User.Role.ADMIN, User.Role.SALES})
    def put(self, request, contact_id, contract_id):
        # check if contact exists
        if not contact_exists(contact_id):
            return Response('Contact not found. Wrong contact_id.', status=status.HTTP_404_NOT_FOUND)

        # check if contract exists
        if not contract_exists(contract_id):
            return Response('Contract not found. Wrong contract_id.', status=status.HTTP_404_NOT_FOUND)

        contract_updated_data = request.data
        contract_to_update = Contract.objects.get(id=contract_id)

        # check if contract belongs to contact
        if not contract_to_update.client_id == contact_id:
            return Response(f"Contract '{contract_id}' does not belong to Client '{contact_id}' !",
                            status=status.HTTP_400_BAD_REQUEST)

        # check if user is owner of contact (ie is sales of the contact)
        user = request.user
        contact = Contact.objects.get(id=contact_id)
        if user.role == User.Role.SALES and not contact.sales_id == user.id:
            return Response('Access forbidden ! You are not attached to the contact or admin.',
                            status=status.HTTP_403_FORBIDDEN)

        serializer = self.serializer_class(contract_to_update, data=contract_updated_data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return JsonResponse(serializer.data, status=status.HTTP_200_OK)

    @user_has_role({User.Role.ADMIN})
    def delete(self, request, contact_id, contract_id):
        # check if contact exists
        if not contact_exists(contact_id):
            return Response('Contact not found. Wrong contact_id.', status=status.HTTP_404_NOT_FOUND)

        # check if contract exists
        if not contract_exists(contract_id):
            return Response('Contract not found. Wrong contract_id.', status=status.HTTP_404_NOT_FOUND)

        contract_to_delete = Contract.objects.get(id=contract_id)

        # check if contract belongs to contact
        if not contract_to_delete.client_id == contact_id:
            return Response(f"Contract '{contract_id}' does not belong to Client '{contact_id}' !",
                            status=status.HTTP_400_BAD_REQUEST)

        contract_to_delete.delete()
        return Response('Contract deleted successfully !', status=status.HTTP_200_OK)
