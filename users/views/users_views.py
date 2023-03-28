from users.serializers.authentication_serializers import UserSerializer
from rest_framework import generics, status
from users.models import User
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated


class UsersViews(generics.GenericAPIView):
    serializer_class = UserSerializer
    permission_classes = ["IsAuthenticated"]

    def get(self, request):
        try:
            user = request.user
            serializer = self.serializer_class(user)
            return Response(
                {
                    "message": "Success",
                    "data": serializer.data,
                    "errors": "null"
                }
                , status=status.HTTP_200_OK
            )
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
