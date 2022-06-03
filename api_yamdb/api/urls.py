from django.urls import path

from api.views import CreateUserAPIView


app_name = 'api'

urlpatterns = [
    path('auth/signup/', CreateUserAPIView.as_view()),
]
