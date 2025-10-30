from django.views.generic import ListView
from ads.models import Ad, Category
from django.db.models import Q

class HomeView(ListView):
    model = Ad
    template_name = "ads/home.html"
    context_object_name = "ads"
    paginate_by = 6 

    def get_queryset(self):
        queryset = (
            Ad.objects.select_related("user", "category")
            .only("title", "description", "price", "location", "image", "created_at", "user__username", "category__name")
            .order_by("-created_at")
        )
        query = self.request.GET.get("q")
        category = self.request.GET.get("category")
        min_price = self.request.GET.get("min_price")
        max_price = self.request.GET.get("max_price")
        location = self.request.GET.get("location")

        if query:
            queryset = queryset.filter(Q(title__icontains=query) | Q(description__icontains=query))
            
        if category:
            queryset = queryset.filter(category__id=category)

        if location:
            queryset = queryset.filter(location__icontains=location)

        if min_price:
            try:
                queryset = queryset.filter(price__gte=float(min_price))
            except ValueError:
                pass  

        if max_price:
            try:
                queryset = queryset.filter(price__lte=float(max_price))
            except ValueError:
                pass

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["categories"] = Category.objects.all()
        return context