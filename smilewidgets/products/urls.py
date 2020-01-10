from django.urls import path
from .views import PriceCalculator

urlpatterns = [
    path('get-price', PriceCalculator.as_view()),
]