from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView
from .models import Ad

class MyAdsView(LoginRequiredMixin, ListView):
    model = Ad
    template_name = 'ads/my_ads.html'
    context_object_name = 'ads'

    def get_queryset(self):
        return Ad.objects.filter(user=self.request.user).order_by('-created_at')

