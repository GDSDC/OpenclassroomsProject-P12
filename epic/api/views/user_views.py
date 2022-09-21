from django.contrib.auth import login, logout
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from api.serializers import LoginSerializer, SignUpSerializer
from api.permissions import isAdmin
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
    permission_classes = (IsAuthenticated, isAdmin)
    serializer_class = SignUpSerializer

    def post(self, request):
        user_to_create = request.data
        serializer = self.serializer_class(data=user_to_create)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class DeleteUserView(APIView):
    """Delete User View"""

    # This view should be accessible only for IsAuthenticated users and Admin users (user.role = 'ADMIN').
    permission_classes = (IsAuthenticated, isAdmin)

    def delete(self, request, user_id):
        # check if user_to_delete exists
        if not user_exists(user_id=user_id):
            return Response('User not found !', status=status.HTTP_404_NOT_FOUND)

        user_to_delete = User.objects.get(id=user_id)
        user_to_delete.delete()
        return Response('User successfully deleted !', status=status.HTTP_200_OK)
