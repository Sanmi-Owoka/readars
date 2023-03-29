from django.urls import path
from .views import BooksListView

urlpatterns = [
    path("", BooksListView.as_view(), name="BooksList")
]