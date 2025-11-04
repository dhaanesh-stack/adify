from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseForbidden, Http404
from django.shortcuts import get_object_or_404
from ads.models import Ad
from .models import Message

class AdAccessMixin(LoginRequiredMixin):
    def setup_ad_access(self, request, *args, **kwargs):
        self.ad = get_object_or_404(Ad, pk=kwargs["pk"])
        self.buyer_id = kwargs.get("buyer_id")
        return request.user

class SellerAccessMixin(AdAccessMixin):
    def check_seller_access(self, user):
        if user.id == self.ad.user_id:
            if not self.buyer_id:
                return Http404()
            try:
                buyer_id_int = int(self.buyer_id)
            except (TypeError, ValueError):
                return Http404()
            if buyer_id_int == user.id:
                return Http404()
            if self.buyer_id and not self.user_model.objects.filter(id=buyer_id_int).exists():
                return Http404()
        return None

class BuyerAccessMixin(AdAccessMixin):
    def check_buyer_access(self, user):
        if user.id != self.ad.user_id:
            if not (Message.objects.filter(ad=self.ad, sender=user).exists() or not self.buyer_id):
                return HttpResponseForbidden()
        return None