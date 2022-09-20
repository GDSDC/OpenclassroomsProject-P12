from django.urls import path

from api.views.user_views import LoginView, LogoutView, SignupView

urlpatterns = [

    path('login/', LoginView.as_view()),
    path('logout/', LogoutView.as_view()),
    path('signup/', SignupView.as_view()),

]
