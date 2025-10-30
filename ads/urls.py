from django.urls import path
from .views import MyAdsView, PostAdView, AdUpdateView,AdDetailView, AdDeleteView

urlpatterns = [
    path("my-ads/", MyAdsView.as_view(), name="my_ads"),
    path('post/', PostAdView.as_view(), name='post_ad'),
    path("<int:pk>/edit/", AdUpdateView.as_view(), name="edit_ad"),
    path('<int:pk>/', AdDetailView.as_view(), name='ad_detail'),
    path('<int:pk>/delete/', AdDeleteView.as_view(), name='delete_ad'),
]
