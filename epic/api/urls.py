from django.urls import path

from api.views.contacts_views import GlobalContactView, ContactView
from api.views.contracts_views import GlobalContractView, ContractView
from api.views.events_views import GlobalEventView
from api.views.user_views import LoginView, LogoutView, SignupView, DeleteUserView

urlpatterns = [

    # 1. auth
    path('users/login/', LoginView.as_view()),
    path('users/logout/', LogoutView.as_view()),
    path('users/signup/', SignupView.as_view()),
    path('users/<int:user_id>/', DeleteUserView.as_view()),

    # 2. contacts
    path('contacts/', GlobalContactView.as_view()),
    path('contacts/<int:contact_id>/', ContactView.as_view()),

    # 3. contracts
    path('contacts/contracts/', GlobalContractView.as_view()),
    path('contacts/<int:contact_id>/contracts/', GlobalContractView.as_view()),
    path('contacts/<int:contact_id>/contracts/<int:contract_id>/', ContractView.as_view()),

    # 4. events
    path('contacts/events/', GlobalEventView.as_view()),
    path('contacts/<int:contact_id>/events/', GlobalEventView.as_view()),

]
