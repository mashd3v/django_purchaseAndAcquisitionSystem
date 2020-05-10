from django.shortcuts import render
from django.utils.dateparse import parse_date
from datetime import timedelta
from .models import BillingDetail, BillingHeader

def printBillingReceipt(request, id):
    template_name = "facturacion/oneBilling.html"
    head = BillingHeader.objects.get(id=id)
    det = BillingDetail.objects.filter(billing=id)
    context = {
        'request':request,
        'head':head,
        'detail':det
    }
    return render(request, template_name, context)

def printBillingList(request, date1, date2):
    template_name = "facturacion/allBillings.html"
    date1 = parse_date(date1)
    date2 = parse_date(date2)
    head = BillingHeader.objects.filter(date__gt=date1, date__lt=date2)
    date2 = date2 - timedelta(days=1)
    context = {
        'request':request,
        'date1':date1,
        'date2':date2,
        'head':head
    }
    return render(request, template_name, context)
