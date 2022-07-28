from django.contrib import admin
from django.urls import path

urlpatterns = [
    path('billing/admin/', admin.site.urls),
]
