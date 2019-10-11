from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import HomeView, ImageGalleryView, ImageView, ImageUploadView

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('view/', ImageGalleryView.as_view(), name='view'),
    path('view/<int:img_id>', ImageView.as_view(), name='image'),
    path('upload/', ImageUploadView.as_view(), name='upload'),
]

if settings.DEBUG:  # Serve media files in development
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
