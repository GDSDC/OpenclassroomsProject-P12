from django.contrib.auth import login, logout
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from api.serializers import LoginSerializer


class LoginView(APIView):
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
    # This view should be accessible only for IsAuthenticated users.
    permission_classes = (IsAuthenticated,)
    serializer_class = LoginSerializer

    def get(self, request):
        user = request.user
        logout(request)
        return Response(f'User {user.email} logged out !', status=status.HTTP_200_OK)
