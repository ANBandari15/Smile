from django.shortcuts import render
from django.views import View
from django.http import HttpResponse
from bson.json_util import dumps
from .models import *
import json

# Create your views here.


class PriceCalculator(View):

    def get(self, request):

        result = {"status": "failed", "message": "productCode must be required"}
        if request.GET["productCode"] != "":
            result["message"] = "date must be required"
            if request.GET["date"] != "":
                result = self.productPrice(request.GET["productCode"], request.GET["date"], request.GET.get("giftCardCode", None))
        return HttpResponse(dumps(result))

    def productPrice(self, product_code, date, gift_card_code=None):

        result = {"status": "failed", "message": ""}
        price = json.loads(dumps(ProductPrice.objects.filter(code=product_code, date_start=date)))
        result["message"] = "price not found"
        if len(price) == 1:
            result.update({"status": "success", "message": "product price", "result": price})
        return result
