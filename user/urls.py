
from django.urls import path
from .views import CustomUserCreateView, UserLoginView


urlpatterns = [
 path('register/', CustomUserCreateView.as_view(), name='user-registration'),
 path('login/', UserLoginView.as_view(), name='login-user')
]
