from users.serializers.authentication_serializers import RegisterSerializer
from rest_framework import generics, status
from users.models import User
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken


class RegisterView(generics.GenericAPIView):
    serializer_class = RegisterSerializer
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
            if serializer.validated_data["password"] != serializer.validated_data["confirm_password"]:
                return Response(
                    {
                        "message": "failure",
                        "data": "null",
                        "errors": "Password does not match confirm_password",
                    }
                    , status=status.HTTP_400_BAD_REQUEST)

            user = User.objects.create(
                email=serializer.validated_data["email"].lower().strip(),
                first_name = serializer.validated_data["first_name"].lower().strip(),
                last_name = serializer.validated_data["last_name"].lower().strip()
            )
            user.set_password(serializer.validated_data["password"])
            user.save()
            auth_token = RefreshToken.for_user(user)

            return Response({
                "message": "Success",
                "data": {
                    "token": str(auth_token.access_token),
                },
                "errors": "null"
            }
                , status=status.HTTP_201_CREATED)
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
