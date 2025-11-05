from django.views.generic import ListView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q, Max, Count, F, Case, When, IntegerField, CharField
from .models import Message
from django.urls import reverse
from collections import defaultdict
from django.utils import timezone
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from .services import send_message
from django.contrib.auth.views import redirect_to_login
from .mixins import SellerAccessMixin, BuyerAccessMixin
from django.http import JsonResponse

class InboxView(LoginRequiredMixin, ListView):
    template_name = "message/inbox.html"
    context_object_name = "conversations"

    def get_queryset(self):
        user = self.request.user
        messages = Message.objects.filter(Q(sender=user) | Q(receiver=user))

        messages_with_other_user = messages.annotate(
            other_user_id=Case(
                When(sender=user, then=F("receiver_id")),
                default=F("sender_id"),
                output_field=IntegerField()
            ),
            other_user_username=Case(
                When(sender=user, then=F("receiver__username")),
                default=F("sender__username"),
                output_field=CharField()
            )
        )

        conversations = messages_with_other_user.values(
            "ad_id", "ad__title", "other_user_id", "other_user_username"
        ).annotate(
            last_msg_time=Max("timestamp"),
            unread_count=Count("id", filter=Q(is_read=False, receiver=user))
        ).order_by("-last_msg_time")

        for conv in conversations:
            conv["chat_url"] = reverse("chat_ad_seller", args=[conv["ad_id"], conv["other_user_id"]])

        return conversations
    
User = get_user_model()


class AdChatView(SellerAccessMixin, BuyerAccessMixin, TemplateView):
    template_name = "message/chat.html"
    user_model = User  
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect_to_login(request.get_full_path())

        user = self.setup_ad_access(request, *args, **kwargs)

        seller_check = self.check_seller_access(user)
        if seller_check:
            return seller_check

        buyer_check = self.check_buyer_access(user)
        if buyer_check:
            return buyer_check

        if request.headers.get("X-Requested-With") == "XMLHttpRequest" and request.GET.get("poll"):
            return self.handle_polling(request)
        return super().dispatch(request, *args, **kwargs)
    
    def _get_chat_partner(self, user):
        if user == self.ad.user:
            if self.buyer_id:
                return get_object_or_404(User, pk=self.buyer_id)
        else:
            return self.ad.user
        return None

    def handle_polling(self, request):
        user = request.user
        last_id = request.GET.get("last_id")

        chat_partner = self._get_chat_partner(user)

        if not chat_partner:
            return JsonResponse([], safe=False)

        messages = (
            Message.objects.filter(ad=self.ad)
            .filter(Q(sender=user, receiver=chat_partner) | Q(sender=chat_partner, receiver=user))
            .order_by("id")
        )

        if last_id and last_id.isdigit():
            messages = messages.filter(id__gt=int(last_id))

        data = [
            {
                "id": msg.id,
                "content": msg.content,
                "sender_name": "You" if msg.sender == user else msg.sender.username,
                "timestamp": timezone.localtime(msg.timestamp).strftime("%H:%M"),
            }
            for msg in messages
        ]

        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user

        chat_partner = self._get_chat_partner(user)

        context["chat_partner"] = chat_partner

        if chat_partner:
            messages = (
                Message.objects.filter(ad=self.ad)
                .filter(Q(sender=user, receiver=chat_partner) | Q(sender=chat_partner, receiver=user))
                .order_by("timestamp")
            )
            messages.filter(receiver=user, is_read=False).update(is_read=True)
        else:
            messages = Message.objects.none()

        grouped_messages = defaultdict(list)
        for msg in messages:
            local_date = timezone.localtime(msg.timestamp).date()
            grouped_messages[local_date].append(msg)

        context["ad"] = self.ad
        context["grouped_messages"] = sorted(grouped_messages.items(), key=lambda item: item[0])
        return context


    def post(self, request, *args, **kwargs):
        return send_message(request, self.ad, self.buyer_id)
