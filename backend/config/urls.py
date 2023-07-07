from django.contrib import admin
from django.urls import path, include

from rest_framework_simplejwt.views import (
    TokenObtainPairView, TokenRefreshView, TokenVerifyView
)


urlpatterns = [
    path('admin/', admin.site.urls),

    path('api/token/', TokenObtainPairView.as_view(), name='get-token'),
    path('api/token/verify/', TokenVerifyView.as_view(), name='verify-token'),
    path('api/token/refresh/',
         TokenRefreshView.as_view(), name='refresh-token'),
    path('api/', include('kanban.router')),
]
