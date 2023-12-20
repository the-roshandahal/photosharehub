from django.urls import path
from . import views
from django.urls import re_path
from django.conf import settings
from django.views.static import serve
from django.conf.urls.static import static  


urlpatterns = [
    path("dashboard", views.dashboard, name="dashboard"),
    path("create_event", views.create_event, name="create_event"),
    path('event/<str:event_credentials>/<str:secret_token>/', views.event, name='event'),
    path('download_qr_code/<str:event_credentials>/<str:secret_token>/', views.download_qr_code, name='download_qr_code'),
    path('delete_event/<str:event_credentials>/', views.delete_event, name='delete_event'),
    path('upload_images/<str:event_credentials>', views.upload_images, name='upload_images'),
    path('folder_detail/<str:folder_credentials>/', views.folder_detail, name='folder_detail'),


    re_path(r"^media/(?P<path>.*)$", serve, {"document_root": settings.MEDIA_ROOT}),
    re_path(r"^static/(?P<path>.*)$", serve, {"document_root": settings.STATIC_ROOT}),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)