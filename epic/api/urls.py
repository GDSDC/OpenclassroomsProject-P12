from django.urls import path

from api.views.contact_views import GlobalContactView
from api.views.user_views import LoginView, LogoutView, SignupView, DeleteUserView


urlpatterns = [

    # 1. auth
    path('users/login/', LoginView.as_view()),
    path('users/logout/', LogoutView.as_view()),
    path('users/signup/', SignupView.as_view()),
    path('users/<int:user_id>/', DeleteUserView.as_view()),

    # 2. contacts
    path('contacts/', GlobalContactView.as_view()),

]
