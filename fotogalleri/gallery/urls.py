from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('view/', views.ImageView.as_view(), name='view'),
    path('upload/', views.ImageUploadView.as_view(), name='upload'),
]

if settings.DEBUG:  # Serve media files in development
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
