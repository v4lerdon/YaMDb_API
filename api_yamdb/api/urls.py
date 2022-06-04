from django.urls import include, path
from rest_framework import routers
from .views import TitleViewSet, GenreViewSet, CategoryViewSet

app_name = 'api'

router = routers.DefaultRouter()

router.register('categories', CategoryViewSet)
router.register('genres', GenreViewSet)
router.register('titles', TitleViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
