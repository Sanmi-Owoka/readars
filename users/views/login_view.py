from rest_framework import generics, status
from users.models import User
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from users.serializers.authentication_serializers import LoginSerializer
from rest_framework.permissions import AllowAny
from django.contrib.auth.hashers import check_password


class LoginView(generics.GenericAPIView):
    serializer_class = LoginSerializer
    permission_classes = [AllowAny]

    def post(self, request):
        try:
            serializer = self.serializer_class(data=request.data)
            if not serializer.is_valid():
                return Response(
                    {
                        "message": "failure",
                        "data": "null",
                        "errors": serializer.errors,
                    }
                    , status=status.HTTP_400_BAD_REQUEST)
            email = serializer.validated_data["email"]
            password = serializer.validated_data["password"]
            check_user_queryset = User.objects.filter(email=email)
            if not check_user_queryset.exists():
                return Response(
                    {
                        "message": "failure",
                        "data": "null",
                        "errors": f"user with email: {email} does not exists",
                    }
                    , status=status.HTTP_404_NOT_FOUND)
            user = check_user_queryset.first()
            if not user.check_password(password):
                return Response(
                    {
                        "message": "failure",
                        "data": "null",
                        "errors": f"Invalid password entered",
                    }
                    , status=status.HTTP_404_NOT_FOUND)
            auth_token = RefreshToken.for_user(user)
            return Response({
                "message": "Success",
                "data": {
                    "email": user.email,
                    "first_name": user.first_name,
                    "last_name": user.last_name,
                    "is_subscribed": user.is_subscribed,
                    "token": str(auth_token.access_token),
                },
                "errors": "null"
            }
                , status=status.HTTP_200_OK)
        except Exception as e:
            print("error", e)
            return Response(
                {
                    "message": "failure",
                    "data": "null",
                    "errors": [f"{e}"]
                }
                , status=status.HTTP_400_BAD_REQUEST
            )
