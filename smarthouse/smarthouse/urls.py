from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path("intercom/", include(("intercom.urls", "intercom"), namespace="intercom"))
]
