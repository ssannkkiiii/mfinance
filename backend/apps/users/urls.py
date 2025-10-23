from django.urls import path
from .views.user import UserViewSet, UserOwnView
from .views.passwords import UserPasswordChangeView, PasswordResetView
from .views.registration import UserRegistrationView, UserProfileCompletionView
from .views.otp import OTPRequestView, OTPVerificationView

app_name = 'users'

urlpatterns = [
    path('', UserViewSet.as_view({'get': 'list'}), name='user-list'),
    path('<int:pk>/', UserViewSet.as_view({'get': 'retrieve'}), name='user-detail'),
    path('me/', UserOwnView.as_view(), name='user-own'),
    path('password/change/', UserPasswordChangeView.as_view(), name='password-change'),
    path('password/reset/', PasswordResetView.as_view(), name='password-reset'),
    path('register/', UserRegistrationView.as_view(), name='user-register'),
    path('complete/', UserProfileCompletionView.as_view(), name='profile-complete'),
    path('otp/request/', OTPRequestView.as_view(), name='otp-request'),
    path('otp/verify/', OTPVerificationView.as_view(), name='otp-verify'),
]