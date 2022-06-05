from django.urls import include, path
from rest_framework import routers
from .views import TitleViewSet, GenreViewSet, CategoryViewSet, UserSignupViewset, UserTokenViewset

app_name = 'api'

router = routers.DefaultRouter()

router.register('categories', CategoryViewSet)
router.register('genres', GenreViewSet)
router.register('titles', TitleViewSet)

urlpatterns = [
    path('v1', include(router.urls)),
    path('v1/auth/signup/', UserSignupViewset.as_view()),
    path('v1/auth/token/', UserTokenViewset.as_view()),
]
