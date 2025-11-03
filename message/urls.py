from django.urls import re_path, path
from .views import InboxView, AdChatView

urlpatterns = [
    path("inbox/", InboxView.as_view(), name='inbox'),
    re_path(r'^(?P<pk>\d+)/chat(?:/(?P<buyer_id>\d+)/)?$', AdChatView.as_view(), name="chat_ad_seller"),
]
