from django.urls import path, include
from rest_framework.routers import SimpleRouter
from api.views import ReviewViewSet, CommentViewSet

router = SimpleRouter()
router.register(
    r'titles/(?P<title_id>\d+)/reviews',
    ReviewViewSet, basename='reviews',)
router.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet, basename='comments',)


app_name = 'api'
urlpatterns = [
    path('v1/', include(router.urls)),
]