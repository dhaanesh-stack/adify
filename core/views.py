from django.views.generic import ListView
from ads.models import Ad

class HomeView(ListView):
    """
    Public homepage that lists all ads with pagination.
    Anonymous users can view ads.
    """
    model = Ad
    template_name = "home.html"
    context_object_name = "ads"
    paginate_by = 6 

    def get_queryset(self):
        return (
            Ad.objects.select_related("user", "category")
            .only("title", "description", "image", "created_at", "user__username", "category__name")
            .order_by("-created_at")
        )
