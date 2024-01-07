from django.urls import path
from .views import *
urlpatterns = [
 path('product/',ProductAPIView.as_view(),name='products'),
 path('product/<int:pk>/',ProductAPIView.as_view(),name='products'),
 path('categories/', CategoryView.as_view(), name='all_categories_and_products'),
 path('categories/<str:category_slug>/', CategoryView.as_view(), name='category_products'),
 path('get-all-categories',AllCategories.as_view(),name="get_all_categories")
]