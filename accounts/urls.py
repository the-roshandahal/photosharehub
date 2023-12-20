from django.urls import path
from . import views
from django.urls import re_path
from django.conf import settings
from django.views.static import serve
from django.conf.urls.static import static  


urlpatterns = [
    path("user_login", views.user_login, name="user_login"),
    path("user_logout", views.user_logout, name="user_logout"),
    path("register", views.register, name="register"),
    path("activation_success", views.activation_success, name="activation_success"),
    path('activate/<str:username>/<str:token>/', views.activate, name='activate'),



    re_path(r"^media/(?P<path>.*)$", serve, {"document_root": settings.MEDIA_ROOT}),
    re_path(r"^static/(?P<path>.*)$", serve, {"document_root": settings.STATIC_ROOT}),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)