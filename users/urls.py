from users import views
from django.urls import path

urlpatterns = [
    path('authorization/', views.AuthorizationAPIView.as_view()),
    path('registration/', views.registration_api_view),
]