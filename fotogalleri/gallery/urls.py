from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.views import LoginView, LogoutView
from .views import HomeView, ImageGalleryView, ImageView, ImageUploadView
from .forms import CustomLoginForm

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('view/', ImageGalleryView.as_view(), name='view'),
    path('view/<int:img_id>', ImageView.as_view(), name='image'),
    path('upload/', ImageUploadView.as_view(), name='upload'),
    path('login/',
         LoginView.as_view(template_name='login.html', authentication_form=CustomLoginForm),
         name='login'),
    path('logout/', LogoutView.as_view(next_page='home'), name='logout'),
]

if settings.DEBUG:  # Serve media files in development
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
