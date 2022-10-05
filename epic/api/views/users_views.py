import logging
from typing import Any, Dict

from django.contrib.auth import login, logout
from django.http import JsonResponse
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from api.serializers import LoginSerializer, SignUpSerializer, UserSerializer
from api.decorators import user_has_role, logging_and_response, query_parameter_parser
from core.users.models import User
from core.users.services import user_exists


class LoginView(APIView):
    """Login View"""

    # This view should be accessible also for unauthenticated users.
    permission_classes = (AllowAny,)
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=self.request.data,
                                           context={'request': self.request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        login(request, user)
        return Response(f'User {user.email} logged in !', status=status.HTTP_202_ACCEPTED)


class LogoutView(APIView):
    """Logout View"""

    # This view should be accessible only for IsAuthenticated users.
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        user = request.user
        logout(request)
        return Response(f'User {user.email} logged out !', status=status.HTTP_200_OK)


class SignupView(APIView):
    """Signup View"""

    # This view should be accessible only for Authenticated Admin users.
    permission_classes = (IsAuthenticated,)
    serializer_class = SignUpSerializer

    @user_has_role({User.Role.ADMIN})
    def post(self, request):
        user_to_create = request.data
        serializer = self.serializer_class(data=user_to_create)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class ManagerUserView(APIView):
    """View or Delete a User View"""

    # This view should be accessible only for IsAuthenticated users and Admin users (user.role = 'ADMIN').
    permission_classes = (IsAuthenticated,)
    serializer_class = UserSerializer

    @user_has_role({User.Role.ADMIN})
    @query_parameter_parser({'role': User.Role})
    def get(self, request, query_params: Dict[str, Any], user_id=None):
        # Looking for a unique User data
        if user_id:
            # check if user exists
            if not user_exists(user_id=user_id):
                return logging_and_response(
                    logger=logging.getLogger('.'.join([__name__, self.__class__.__name__, self.get.__name__])),
                    error_message=f"User '{user_id}' not found. Wrong contact_id.",
                    error_status=status.HTTP_404_NOT_FOUND)
            users = User.objects.get(id=user_id)
            is_many = False
        else:
            # Looking for multiple Users data
            users = User.objects.filter(**query_params)
            is_many = True
        return JsonResponse(self.serializer_class(users, many=is_many).data, status=status.HTTP_200_OK, safe=False)

    @user_has_role({User.Role.ADMIN})
    def delete(self, request, user_id):
        # check if user_to_delete exists
        if not user_exists(user_id=user_id):
            return logging_and_response(
                logger=logging.getLogger('.'.join([__name__, self.__class__.__name__, self.delete.__name__])),
                error_message=f"User '{user_id}' not found. Wrong contact_id.",
                error_status=status.HTTP_404_NOT_FOUND)

        user_to_delete = User.objects.get(id=user_id)
        user_to_delete.delete()
        return Response('User successfully deleted !', status=status.HTTP_200_OK)
