from rest_framework import serializers
from books.models import Book
from users.serializers.authentication_serializers import UserSerializer


class CreateBookSerializer(serializers.ModelSerializer):
    title = serializers.CharField(max_length=68, min_length=1)
    description = serializers.CharField(max_length=2555, min_length=1)
    
    class Meta:
        model = Book
        fields = [
            "title",
            "description",
            "doc",
            "thumbnail",
        ]

class BookSerializer(serializers.ModelSerializer):
    author = UserSerializer()
    thumbnail = serializers.SerializerMethodField()
    doc = serializers.SerializerMethodField()

    class Meta:
        model = Book
        fields = [
            "id",
            "title",
            "description",
            "author",
            "thumbnail",
            "doc",
            "updated_at",
            "created_at"
        ]
        read_only_fields = [
            "id",
            "title",
            "description",
            "author",
            "thumbnail",
            "updated_at",
            "created_at"
        ]

    def get_thumbnail(self, instance):
        try:
            return self.context["request"].build_absolute_uri(instance.thumbnail.url)
        except:
            return None
        
    def get_doc(self, instance):
        try:
            return self.context["request"].build_absolute_uri(instance.doc.url)
        except:
            return None


class UpdateBookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = [
            "id",
            "title",
            "description",
            "thumbnail",
            "updated_at",
            "created_at"
        ]
        read_only_fields = [
            "id",
            "updated_at",
            "created_at"
        ]