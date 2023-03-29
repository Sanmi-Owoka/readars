from books.views import BooksViewSet
from rest_framework.routers import DefaultRouter, SimpleRouter
from django.conf import settings

if settings.DEBUG:
    router = DefaultRouter()
else:
    router = SimpleRouter()

router.register("books", BooksViewSet, basename="books")

app_name = "READERS"
urlpatterns = router.urls