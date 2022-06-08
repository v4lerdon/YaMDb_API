from django.urls import include, path
from rest_framework.routers import DefaultRouter

from api.views import (UserMeRetrieveUpdate, UserSignupViewset,
                       UsersSettingsViewset, UserTokenViewset)

app_name = 'api'

router = DefaultRouter()

router.register(r'users', UsersSettingsViewset, basename='usersettings')

urlpatterns = [
    path('v1/auth/signup/', UserSignupViewset.as_view()),
    path('v1/auth/token/', UserTokenViewset.as_view()),
    path('v1/users/me/', UserMeRetrieveUpdate.as_view()),
    path('v1/', include(router.urls)),
]
