from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q, Max, Count, F, Case, When, IntegerField, CharField
from .models import Message

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

        return conversations
    