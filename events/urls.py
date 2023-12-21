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
    path('save_event/<str:event_credentials>', views.save_event, name='save_event'),
    path('unsave_event/<str:event_credentials>', views.unsave_event, name='unsave_event'),
    path('all_images/<str:event_credentials>', views.all_images, name='all_images'),
    path('saved_events/<int:id>', views.saved_events, name='saved_events'),


    re_path(r"^media/(?P<path>.*)$", serve, {"document_root": settings.MEDIA_ROOT}),
    re_path(r"^static/(?P<path>.*)$", serve, {"document_root": settings.STATIC_ROOT}),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)