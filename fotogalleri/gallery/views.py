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


class ImageGalleryView(ListView):
    model = ImageMetadata
    template = 'view_images.html'

    def get(self, request):
        context = {'object_list': self.model.objects.all()}
        return render(request, self.template, context)


class ImageView(View):
    template = 'image.html'
    model = ImageMetadata

    def get(self, request, img_id):
        context = {'image': self.model.objects.get(pk=img_id)}
        return render(request, self.template, context)


class ImageUploadView(CreateView):
    model = ImageMetadata
    form_class = ImageUploadForm
    template_name = 'upload_image.html'
    success_url = reverse_lazy('view')
