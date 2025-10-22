from django.urls import path
from .views import (
    AdListView,
    PostAdView,
    MyAdsView,
    AdUpdateView,
    AdDeleteView,
)

urlpatterns = [
    path('', AdListView.as_view(), name='ad_list'),          
    path('post/', PostAdView.as_view(), name='post_ad'),     
    path('my-ads/', MyAdsView.as_view(), name='my_ads'),     
    path('<int:pk>/edit/', AdUpdateView.as_view(), name='edit_ad'),  
    path('<int:pk>/delete/', AdDeleteView.as_view(), name='delete_ad'),  
]
