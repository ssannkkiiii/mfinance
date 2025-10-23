from django.urls import path
from apps.authentication.views.authentication import UserLoginView, LogoutView
from apps.authentication.google_auth.google_authentication import GoogleLoginInitView, GoogleLoginCallbackView

app_name = 'authentication'

urlpatterns = [
    path('login/', UserLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('google/login/', GoogleLoginInitView.as_view(), name='google-login'),
    path('google/callback/', GoogleLoginCallbackView.as_view(), name='google-callback'),
]