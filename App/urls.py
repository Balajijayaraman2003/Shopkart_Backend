from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import (
    ProductView, ProductDetailedView, SearchProductView,
    RetriveSimilarProductsView, CategoriesView, ProductBasedOnCategoriesView,
    ReviewsView, ReviewsCreateView, TopDealsView, NewArrivalsView,
    WhishListView, CartView,WishListDestroyView
)

router = DefaultRouter()
router.register(r"cart", CartView, basename="cart")

urlpatterns = [
    path("products/", ProductView.as_view(), name="product-list"),
    path("products/<str:code>", ProductDetailedView.as_view(), name="product-detail"),
    path("products/search/", SearchProductView.as_view(), name="search-products"),
    path("products/similar/<str:code>", RetriveSimilarProductsView.as_view(), name="similar-products"),
    path("categories/", CategoriesView.as_view(), name="categories"),
    path("category-products/<str:id>", ProductBasedOnCategoriesView.as_view(), name="category-products"),
    
    path("reviews/<str:code>", ReviewsView.as_view(), name="review-detail"),
    path("reviews/", ReviewsCreateView.as_view(), name="review-create"),
    
    path("deals/", TopDealsView.as_view(), name="top-deals"),
    path("arrivals/", NewArrivalsView.as_view(), name="new-arrivals"),
    path("whishlist/", WhishListView.as_view(), name="wishlist"),
    path("whishlist/<int:pk>", WishListDestroyView.as_view(), name="wishlist"),
]

# Add router-generated URLs
urlpatterns += router.urls