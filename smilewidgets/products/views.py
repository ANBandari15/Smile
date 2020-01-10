from django.shortcuts import render
from django.views import View
from django.http import HttpResponse
from bson.json_util import dumps
from django.db.models import *
from .models import *
import json

# Create your views here.


class PriceCalculator(View):

    def get(self, request):

        result = {"status": "failed", "message": "productCode must be required"}
        if request.GET["productCode"] != "":
            result["message"] = "date must be required"
            if request.GET["date"] != "":
                result = self.product_price(request.GET["productCode"], request.GET["date"], request.GET.get("giftCardCode", None))
        return HttpResponse(dumps(result))

    # @staticmethod
    def product_price(self, product_code, date, gift_card_code):

        result = {"status": "failed", "message": ""}
        product_price = Product.objects.filter(code=product_code).values("price")
        result["message"] = "Invalid product code"
        if len(product_price) == 1:
            if gift_card_code:
                gift_card_price = GiftCard.objects.filter(Q(date_end=None) | Q(date_end__lte=date), code=gift_card_code, date_start__gte=date).values("amount")
                result["message"] = "Invalid gift card code"
                if len(gift_card_price) == 1:
                    price = product_price[0]["price"]-gift_card_price[0]["amount"]
                    result.update({"status": "success", "message": "product price", "result": price})
            else:
                price = json.loads(dumps(ProductPrice.objects.filter(code=product_code, offer_date=date).values("price")))
                if len(price) == 1:
                    price = price[0]["price"]
                    result.update({"status": "success", "message": "product price", "result": price})
                else:
                    gift_card_price = GiftCard.objects.filter(Q(date_end=None) | Q(date_end__lte=date), date_start__gte=date).values("amount")
                    result["message"] = "price not found"
                    if len(gift_card_price) == 1:
                        price = product_price[0]["price"] - gift_card_price[0]["amount"]
                        result.update({"status": "success", "message": "product price", "result": price})
        return result

