from rest_framework import status, generics
from rest_framework.viewsets import GenericViewSet
from rest_framework.response import Response
from .serializers import BookSerializer, UpdateBookSerializer, CreateBookSerializer
from django.core.exceptions import ObjectDoesNotExist
from config.functools import paginate
from django.db.models import Q
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework import filters
from decimal import Decimal
from .models import Book


class BooksListView(generics.ListAPIView):
    serializer_class = BookSerializer
    queryset = Book.objects.all().order_by("-created_at")
    permission_classes = [AllowAny]
    filter_backends = [filters.SearchFilter]
    search_fields = ["title", "author__author_pseudonym", "author__username"]


class BooksViewSet(GenericViewSet):
    serializer_class = BookSerializer
    queryset = Book.objects.all()

    @action(detail=False, methods=["POST"], name='create book', serializer_class=CreateBookSerializer)
    def create_book(self, request):
        try:
            # create book endpoint
            user = request.user
            title = request.data["title"]
            description = request.data["description"]
            thumbnail = request.data["thumbnail"]
            serializer = self.serializer_class(data=request.data)
            if not serializer.is_valid():
                return Response(
                    {
                        "message": "failure",
                        "data": "null",
                        "errors": serializer.errors,
                    }
                    , status=status.HTTP_400_BAD_REQUEST)

            if Book.objects.filter(title=title).exists():
                return Response({"message": ["Book with title already exits"]}, status=status.HTTP_400_BAD_REQUEST)
            new_book = Book.objects.create(
                title=title,
                description=description,
                thumbnail=thumbnail,
                author=user
            )
            response = BookSerializer(new_book)
            return Response(response.data, status=status.HTTP_201_CREATED)
        except KeyError as e:
            print("error", e)
            return Response(
                {"message": [f"{e} field is required"]}, status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            print("error", e)
            return Response({"message": [f"{e}"]}, status=status.HTTP_400_BAD_REQUEST)

    def list(self, request):
        try:
            # overidden the get endpoint to list all users books
            user = request.user
            search = request.GET.get('search', None)
            if search:
                get_books = Book.objects.filter(Q(author=user) & Q(title__icontains=search)).order_by('-created_at')
            else:
                get_books = Book.objects.filter(author=user).order_by('-created_at')
            return Response(
                paginate(
                    get_books,
                    int(request.query_params.get("page", 1)),
                    self.get_serializer,
                    {"request": request},
                    int(request.query_params.get("limit", 10)),
                ), status=status.HTTP_200_OK
            )
        except Exception as e:
            print("error", e)
            return Response({"message": [f"{e}"]}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=["GET"], serializer_class=BookSerializer, name='get user books')
    def get_user_books(self, request):
        try:
            user = request.user
            user_books = Book.objects.filter(author=user)
            if not user_books.exists():
                return Response([], status=status.HTTP_200_OK)
            response = self.get_serializer(user_books, many=True)
            return Response(response.data, status=status.HTTP_200_OK)
        except Exception as e:
            print("error", e)
            return Response({"message": [f"{e}"]}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=["GET"], name='get specific book')
    def get_book(self, request):
        try:
            # endpoint to get specifi book details
            user = request.user
            book_id = request.GET.get('id')
            try:
                get_book_obj = Book.objects.get(author=user, id=book_id)
            except ObjectDoesNotExist:
                return Response({"message": [f"book with id: {book_id} does not exists"]}
                                , status=status.HTTP_404_NOT_FOUND)
            serializer = self.get_serializer(get_book_obj)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            print("error", e)
            return Response({"message": [f"{e}"]}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=["PUT"], serializer_class=UpdateBookSerializer, name='update book')
    def update_book(self, request):
        try:
            # endpoint to update users book with book id endpoint
            user = request.user
            book_id = request.data["book_id"]
            if not book_id:
                return Response({"message": ["book_id field is required"]}, status=status.HTTP_400_BAD_REQUEST)
            try:
                get_book = Book.objects.get(author=user, id=book_id)
            except ObjectDoesNotExist:
                return Response(
                    {
                        "message": [f"Book with id: {book_id} does not exists"]
                    },
                    status=status.HTTP_404_NOT_FOUND,
                )
            serializer = self.get_serializer(get_book, data=request.data, partial=True)
            if not serializer.is_valid():
                return Response({"message": [serializer.errors]}, status=status.HTTP_400_BAD_REQUEST)
            serializer.save()
            return Response(
                serializer.data,
                status=status.HTTP_206_PARTIAL_CONTENT
            )
        except Exception as e:
            print("error", e)
            return Response({"message": [f"{e}"]}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=["DELETE"], name='delete book')
    def delete_book(self, request):
        try:
            # endpoint to delete book using book_id being provided
            user = request.user
            book_id = request.GET.get("book_id", None)
            if not book_id:
                return Response({"message": ["book_id query parameter is required"]},
                                status=status.HTTP_400_BAD_REQUEST)
            try:
                get_book = Book.objects.get(author=user, id=book_id)
            except ObjectDoesNotExist:
                return Response({"message": [f"book with id: {book_id} does not exists"]}
                                , status=status.HTTP_404_NOT_FOUND)
            get_book.delete()
            return Response({"message": [f"book with id: {book_id} has been successfully deleted"]}
                            , status.HTTP_204_NO_CONTENT)
        except Exception as e:
            print("error", e)
            return Response({"message": [f"{e}"]}, status=status.HTTP_400_BAD_REQUEST)


# Create your views here.
