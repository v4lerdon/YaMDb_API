from django.urls import path

from api.views import UserSignupViewset, UserTokenViewset


app_name = 'api'

urlpatterns = [
    path('v1/auth/signup/', UserSignupViewset.as_view()),
    path('v1/auth/token/', UserTokenViewset.as_view())
]
