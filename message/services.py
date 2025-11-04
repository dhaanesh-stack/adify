from django.shortcuts import get_object_or_404, redirect
from django.http import JsonResponse
from django.contrib.auth import get_user_model
from .models import Message

User = get_user_model()


def send_message(request, ad, buyer_id=None):
    user = request.user
    content = request.POST.get("content", "").strip()
    is_ajax = request.headers.get("x-requested-with") == "XMLHttpRequest"

    if not content:
        if is_ajax:
            return JsonResponse({"error": "Message cannot be empty"}, status=400)
        return redirect(request.path)

    if user.id == ad.user_id:
        if not buyer_id:
            if is_ajax:
                return JsonResponse({"error": "Buyer not specified."}, status=400)
            return redirect(request.path)
        receiver = get_object_or_404(User, pk=buyer_id)
    else:
        receiver = ad.user

    msg = Message.objects.create(sender=user, receiver=receiver, ad=ad, content=content)

    if is_ajax:
        return JsonResponse(
            {
                "id": msg.id,
                "sender": msg.sender.username,
                "sender_id": msg.sender_id,
                "content": msg.content,
                "timestamp": msg.timestamp.strftime("%H:%M"),
            }
        )

    return redirect(request.path)