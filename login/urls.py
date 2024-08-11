from django.urls import path
from .views import TokenView, UserView

urlpatterns = [
    path('token/', TokenView.as_view()),
    path('me/', UserView.as_view()),
]
