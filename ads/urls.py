from django.urls import path
from .views import MyAdsView,PostAdView

urlpatterns = [
    path("my-ads/", MyAdsView.as_view(), name="my_ads"),
    path('post/', PostAdView.as_view(), name='post_ad'),
]
