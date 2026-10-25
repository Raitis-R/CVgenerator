from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import include, path

from cvapp.api import router

urlpatterns = [
    path("admin/", admin.site.urls),                               # CMS
    path("login/", auth_views.LoginView.as_view(), name="login"),  # autorizācija
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
    path("api/", include(router.urls)),                            # REST serviss
    path("api-auth/", include("rest_framework.urls")),             # DRF pieteikšanās
    path("", include("cvapp.urls")),
]
