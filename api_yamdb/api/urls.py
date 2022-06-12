from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (CategoryViewSet, CommentViewSet, GenreViewSet,
                    ReviewViewSet, TitleViewSet, UserMeRetrieveUpdate,
                    UserSignupViewset, UsersSettingsViewset, UserTokenViewset)

app_name = 'api'

router = DefaultRouter()

router.register(
    r'titles/(?P<title_id>\d+)/reviews',
    ReviewViewSet,
    basename='reviews'
)
router.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet,
    basename='comments',
)
router.register('categories', CategoryViewSet)
router.register('genres', GenreViewSet)
router.register('titles', TitleViewSet)
router.register('users', UsersSettingsViewset, basename='usersettings')

urlpatterns = [
    path('v1/auth/signup/', UserSignupViewset.as_view()),
    path('v1/auth/token/', UserTokenViewset.as_view()),
    path('v1/users/me/', UserMeRetrieveUpdate.as_view()),
    path('v1/', include(router.urls)),
]
