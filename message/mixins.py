from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseForbidden, Http404
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from ads.models import Ad
from .models import Message

User = get_user_model()

class AdAccessMixin(LoginRequiredMixin):
    def setup_ad_access(self, request, *args, **kwargs):
        ad_pk = kwargs.get("pk") or kwargs.get("ad_id")
        self.ad = get_object_or_404(Ad, pk=ad_pk)
        self.buyer_id = kwargs.get("buyer_id")
        return request.user

class SellerAccessMixin(AdAccessMixin):
    def check_seller_access(self, user):
        if user.id == self.ad.user_id:
            if not self.buyer_id:
                raise Http404()
            try:
                buyer_id_int = int(self.buyer_id)
            except (TypeError, ValueError):
                raise Http404()
            if buyer_id_int == user.id:
                raise Http404()
            if not User.objects.filter(id=buyer_id_int).exists():
                raise Http404()
        return None

class BuyerAccessMixin(AdAccessMixin):
    def check_buyer_access(self, user):
        if user.id != self.ad.user_id:
            if not (Message.objects.filter(ad=self.ad, sender=user).exists() or self.buyer_id):
                return HttpResponseForbidden()
        return None