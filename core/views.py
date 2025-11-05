from django_filters.views import FilterView
from ads.models import Ad, Category
from ads.filters import AdFilter

class HomeView(FilterView):
    model = Ad
    template_name = "ads/home.html"
    context_object_name = "ads"
    paginate_by = 6
    filterset_class = AdFilter

    def get_queryset(self):
        queryset = (
            Ad.objects.select_related("user", "category")
            .only("title", "description", "price", "location", "image", "created_at", "user__username", "category__name")
            .order_by("-created_at")
        )
        return self.filterset_class(self.request.GET, queryset=queryset).qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["categories"] = Category.objects.all()
        context["filter"] = self.filterset_class(self.request.GET, queryset=self.get_queryset())
        return context
