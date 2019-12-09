from django.urls import path, re_path
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.views import LoginView, LogoutView
from .views import HomeView, ImageGalleryView, ImageView, ImageUploadView, NewFolderView, DeleteObject, Feedback
from .forms import CustomLoginForm

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    re_path(r'^view/', ImageGalleryView.as_view(), name='view'),
    path('image/<int:img_id>', ImageView.as_view(), name='image'),
    re_path(r'^upload/$', ImageUploadView.as_view(), name='upload'),
    re_path(r'^newfolder/$', NewFolderView.as_view(), name='newfolder'),
    re_path(r'^delete/$', DeleteObject.as_view(), name='delete'),
    re_path(r'^feedback/$', Feedback.as_view(), name='feedback'),
    path('login/',
         LoginView.as_view(template_name='login.html', authentication_form=CustomLoginForm),
         name='login'),
    path('logout/', LogoutView.as_view(next_page='home'), name='logout'),
]

if settings.DEBUG:  # Serve media files in development
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
