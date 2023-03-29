from users.models import User
from rest_framework import serializers


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=68, min_length=6, write_only=True)
    confirm_password = serializers.CharField(max_length=68, min_length=6, write_only=True)
    email = serializers.EmailField(required=True)
    first_name = serializers.CharField(max_length=68, min_length=1)
    last_name = serializers.CharField(max_length=68, min_length=1)

    class Meta:
        model = User
        fields = [
            "email",
            "password",
            "confirm_password",
            "first_name",
            "last_name"
        ]

    def validate(self, attrs):
        email = attrs.get("email", "")
        
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError({"email": f"user with email: {email} already exists"})
        
        return attrs

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class UserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=False)
    

    class Meta:
        model = User
        fields = [
            "id",
            "email",
            "date_joined",
        ]
        read_only_fields = [
            "id",
            "date_joined"
        ]


class LoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(max_length=68, min_length=6, write_only=True, required=True)

    class Meta:
        model = User
        fields = [
            "email",
            "password",
        ]
