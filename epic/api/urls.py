from django.urls import path

from api.views.clients_views import GlobalClientView, ClienttView
from api.views.contracts_views import GlobalContractView, ContractView
from api.views.events_views import GlobalEventView, EventView
from api.views.users_views import LoginView, LogoutView, SignupView, ManagerUserView

urlpatterns = [

    # 1. auth
    path('users/', ManagerUserView.as_view()),
    path('users/<int:user_id>/', ManagerUserView.as_view()),
    path('users/signup/', ManagerUserView.as_view()),
    path('users/login/', LoginView.as_view()),
    path('users/logout/', LogoutView.as_view()),


    # 2. clients
    path('clients/', GlobalClientView.as_view()),
    path('clients/<int:client_id>/', ClienttView.as_view()),

    # 3. contracts
    path('clients/contracts/', GlobalContractView.as_view()),
    path('clients/<int:client_id>/contracts/', GlobalContractView.as_view()),
    path('clients/<int:client_id>/contracts/<int:contract_id>/', ContractView.as_view()),

    # 4. events
    path('clients/events/', GlobalEventView.as_view()),
    path('clients/<int:client_id>/events/', GlobalEventView.as_view()),
    path('clients/<int:client_id>/events/<int:event_id>/', EventView.as_view()),

]
