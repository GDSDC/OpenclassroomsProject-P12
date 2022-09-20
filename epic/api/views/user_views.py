from django.contrib.auth import login, logout
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from api.serializers import LoginSerializer, SignUpSerializer


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
    serializer_class = LoginSerializer

    def get(self, request):
        user = request.user
        logout(request)
        return Response(f'User {user.email} logged out !', status=status.HTTP_200_OK)


class SignupView(APIView):
    """Signup View"""

    # This view should be accessible only for IsAuthenticated users and Admin users (user.role = 'ADMIN').
    permission_classes = (IsAuthenticated,)
    serializer_class = SignUpSerializer

    def post(self, request):

        # check if user is admin
        user = request.user
        if user.role != 'ADMIN':
            return Response('Access Forbidden !', status=status.HTTP_403_FORBIDDEN)

        user_to_create = request.data
        serializer = self.serializer_class(data=user_to_create)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    # TODO : handle     Access Forbidden