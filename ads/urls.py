from django.urls import path
from .views import MyAdsView

urlpatterns = [
    path("my-ads/", MyAdsView.as_view(), name="my_ads"),
]
