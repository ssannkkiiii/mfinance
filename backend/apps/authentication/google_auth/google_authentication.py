from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from django.conf import settings
from rest_framework import status
import requests
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken

User = get_user_model()

class GoogleLoginInitView(APIView):
    
    permission_classes = [AllowAny]
    
    def get(self, request):
        auth_url = (
            f"{settings.GOOGLE_AUTH_URI}"
            f"?client_id={settings.GOOGLE_CLIENT_ID}"
            f"&redirect_uri={settings.GOOGLE_REDIRECT_URL}"
            f"&response_type=code"
            f"&scope=openid%20email%20profile"
        )
        return Response({"auth_url": auth_url})
    
class GoogleLoginCallbackView(APIView):
    
    permission_classes = [AllowAny]
    
    def get(self, request):
        code = request.GET.get("code")
        if not code:
            return Response({"error": "No code provided"}, status=status.HTTP_400_BAD_REQUEST)

        token_data = {
            "code": code,
            "client_id": settings.GOOGLE_CLIENT_ID,
            "client_secret": settings.GOOGLE_CLIENT_SECRET,
            "redirect_uri": settings.GOOGLE_REDIRECT_URL,
            "grant_type": "authorization_code",
        }
        try:
            token_resp = requests.post(settings.GOOGLE_TOKEN_URI, data=token_data)
            token_resp.raise_for_status()
            token_json = token_resp.json()
        except requests.RequestException as e:
            return Response({"error": "Failed to get token from Google"}, status=status.HTTP_400_BAD_REQUEST)

        if "error" in token_json:
            return Response(token_json, status=status.HTTP_400_BAD_REQUEST)

        access_token = token_json["access_token"]

        try:
            userinfo_resp = requests.get(
                settings.GOOGLE_USERINFO_URI,
                headers={"Authorization": f"Bearer {access_token}"},
            )
            userinfo_resp.raise_for_status()
            userinfo = userinfo_resp.json()
        except requests.RequestException as e:
            return Response({"error": "Failed to get user info from Google"}, status=status.HTTP_400_BAD_REQUEST)

        email = userinfo.get("email")
        name = userinfo.get("name")
        picture = userinfo.get("picture")

        if not email:
            return Response({"error": "No email from Google"}, status=status.HTTP_400_BAD_REQUEST)

        name_parts = name.split() if name else []
        first_name = name_parts[0] if name_parts else ""
        last_name = " ".join(name_parts[1:]) if len(name_parts) > 1 else ""
        
        user, created = User.objects.get_or_create(
            email=email, 
            defaults={
                "first_name": first_name,
                "last_name": last_name
            }
        )

        refresh = RefreshToken.for_user(user)
        return Response({
            "refresh": str(refresh),
            "access": str(refresh.access_token),
            "user": {
                "email": email,
                "name": name,
                "picture": picture,
            }
        })