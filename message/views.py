from django.views.generic import ListView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q, Max, Count, F, Case, When, IntegerField, CharField
from .models import Message
from ads.models import Ad
from django.http import JsonResponse, HttpResponseForbidden
from django.urls import reverse
from collections import defaultdict
from django.utils import timezone
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model

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


class AdChatView(LoginRequiredMixin, TemplateView):
    template_name = "message/chat.html"

    def dispatch(self, request, *args, **kwargs):
        self.ad = get_object_or_404(Ad, pk=kwargs["pk"])
        self.buyer_id = kwargs.get("buyer_id")
        user = request.user

        if not user.is_authenticated:
            from django.contrib.auth.views import redirect_to_login

            return redirect_to_login(request.get_full_path())

        if user.id == self.ad.user_id and not self.buyer_id:
            return JsonResponse(
                {"error": "You cannot message your own ad."}, status=403
            )

        if user.id == self.ad.user_id and self.buyer_id:
            if not User.objects.filter(id=self.buyer_id).exists():
                return HttpResponseForbidden()

        if user.id != self.ad.user_id:
            if (
                Message.objects.filter(ad=self.ad, sender=user).exists()
                or not self.buyer_id
            ):
                pass
            else:
                return HttpResponseForbidden()

        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user

        chat_partner = None
        if user == self.ad.user:
            if self.buyer_id:
                chat_partner = get_object_or_404(User, pk=self.buyer_id)
        else:
            chat_partner = self.ad.user

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
        user = request.user
        content = request.POST.get("content", "").strip()
        if not content:
            return JsonResponse({"error": "Message cannot be empty"}, status=400)

        if user.id == self.ad.user_id:
            if not self.buyer_id:
                return JsonResponse({"error": "Buyer not specified."}, status=400)
            receiver = get_object_or_404(User, pk=self.buyer_id)
        else:
            receiver = self.ad.user

        msg = Message.objects.create(
            sender=user, receiver=receiver, ad=self.ad, content=content
        )

        return JsonResponse(
            {
                "sender": msg.sender.username,
                "content": msg.content,
                "timestamp": msg.timestamp.strftime("%H:%M"),
            }
        )
