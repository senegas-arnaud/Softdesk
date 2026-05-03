from django.contrib import admin
from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from users.views import RegisterView, UserDetailView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/users/register/', RegisterView.as_view(), name='register'),
    path('api/users/login/', TokenObtainPairView.as_view(), name='login'),
    path('api/users/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/users/me/', UserDetailView.as_view(), name='user-detail'),
]
