from django.shortcuts import render
from django.views.generic import CreateView, ListView
from django.views import View
from django.urls import reverse_lazy
from backend.models import ImageMetadata
from gallery.forms import ImageUploadForm


class HomeView(View):
    template = 'base.html'

    def get(self, request):
        context = {}
        return render(request, self.template, context)


class ImageView(ListView):
    model = ImageMetadata
    template_name = 'view_images.html'


class ImageUploadView(CreateView):
    model = ImageMetadata
    form_class = ImageUploadForm
    template_name = 'upload_image.html'
    success_url = reverse_lazy('view')
