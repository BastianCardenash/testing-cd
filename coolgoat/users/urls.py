from django.urls import path
from .views import WalletUpdateView, UserCreateView, UserGetView

urlpatterns = [
    path('create/', UserCreateView.as_view(), name='user_create'),
    path('<str:user_email>/', UserGetView.as_view(), name='user_get'),
    path('<str:user_email>/wallet/', WalletUpdateView.as_view(), name='wallet_update'),
]
