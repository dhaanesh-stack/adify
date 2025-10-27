from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from .models import Ad
from .forms import AdForm

class MyAdsView(LoginRequiredMixin, ListView):
    model = Ad
    template_name = 'ads/my_ads.html'
    context_object_name = 'ads'

    def get_queryset(self):
        return Ad.objects.filter(user=self.request.user).order_by('-created_at')

class PostAdView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Ad
    form_class = AdForm
    template_name = 'ads/post_ad.html'
    success_url = reverse_lazy('my_ads')
    success_message = "Your ad has been posted successfully!"

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class AdUpdateView(
    LoginRequiredMixin, UserPassesTestMixin, SuccessMessageMixin, UpdateView
):
    model = Ad
    form_class = AdForm
    template_name = "ads/edit_ad.html"
    success_url = reverse_lazy("my_ads")
    success_message = "Your ad has been updated successfully!"

    def test_func(self):
        ad = self.get_object()
        return self.request.user == ad.user


class AdDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Ad
    template_name = 'ads/confirm_delete.html'
    success_url = reverse_lazy('my_ads')

    def test_func(self):
        ad = self.get_object()
        return self.request.user == ad.user