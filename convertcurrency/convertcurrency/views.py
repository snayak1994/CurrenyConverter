import requests
from django.shortcuts import render
from django.http import HttpResponse
from django.conf import settings

def get_exchange_rate(base_currency, target_currency):
    api_response = requests.get(settings.API_URI)
    if api_response.status_code == 200:
        return api_response.json()["rates"][target_currency],api_response.json()["rates"][base_currency]

def convertCurrency(request):
    api_response = requests.get(settings.API_URI)
    if api_response.status_code == 200:
        currencyList = api_response.json()["rates"].keys()
    else:
        currencyList = []
    if request.method == 'GET':
        return render(request,"form.html",{"currencyList":currencyList})
    elif request.method == 'POST':
        try:
            status = "OK"
            base_currency = request.POST.get("source")
            target_currency = request.POST.get("target")
            amount = request.POST.get("amount")
            try:
                amounttoconvert = float(amount)
            except Exception,e:
                raise Exception("Please enter valid amount")
            if base_currency == 0:
                result = 0
            elif base_currency == target_currency:
                result = 1
            elif base_currency == "EUR":
                target,base = get_exchange_rate(base_currency, target_currency)
                result = target
            else:
                target,base = get_exchange_rate(base_currency, target_currency)
                result = target/base
            convertedAmount = result * float(amount)
            return render(request,"form.html",{"currencyList":currencyList,"result":convertedAmount,"base":base_currency,"target":target_currency,"amount":amount,"status":"OK"})
        except Exception,e:
            status = "FAIL"
            return render(request,"form.html",{"currencyList":currencyList,"status":status,"message":"Please enter valid amount"})
