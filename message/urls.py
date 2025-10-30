from django.urls import path
from .views import (
    InboxView,
    AdChatView,
)


urlpatterns = [
    path("inbox/", InboxView.as_view(), name='inbox'),
    path("<int:pk>/chat/", AdChatView.as_view(), name="chat_ad"),
    path(
        "<int:pk>/chat/<int:buyer_id>/", AdChatView.as_view(), name="chat_ad_seller"
    ),
]
