from django.shortcuts import render, redirect
from django.views import generic
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.http import HttpResponse
from datetime import datetime
from django.contrib.auth.decorators import login_required, permission_required
from .forms import CustomerForm
from .models import Customer, BillingDetail, BillingHeader, Product
from bases.views import NoPermission
import inventario.views as inv
from django.contrib import messages
from django.contrib.auth import authenticate

class CustomerView(NoPermission, generic.ListView):
    model = Customer
    template_name = "facturacion/customerList.html"
    context_object_name = "obj"
    permission_required = "compras.view_customer"

class MainCreateView(SuccessMessageMixin, NoPermission, generic.CreateView):
    context_object_name = 'obj'
    success_message = "Register Added Successfully"
    def form_valid(self, form):
        form.instance.userCreator = self.request.user
        return super().form_valid(form)

class MainUpdateView(SuccessMessageMixin, NoPermission, generic.UpdateView):
    context_object_name = 'obj'
    success_message = "Register Updated Successfully"
    def form_valid(self, form):
        form.instance.userModifier = self.request.user.id
        return super().form_valid(form)

class NewCustomer(MainCreateView):
    model = Customer
    template_name = "facturacion/customerForm.html"
    form_class = CustomerForm
    success_url = reverse_lazy("facturacion:customerList")
    permission_required = "facturacion.add_customer"

class UpdateCustomer(MainUpdateView):
    model = Customer
    template_name = "facturacion/customerForm.html"
    form_class = CustomerForm
    success_url = reverse_lazy("facturacion:customerList")
    permission_required = "facturacion.change_customer"

@login_required(login_url="/login/")
@permission_required("facturacion.change_customer", login_url="/login/")
def deactivateCustomer(request, id):
    customer = Customer.objects.filter(pk=id).first()
    if request.method == "POST":
        if customer:
            customer.status = not customer.status
            customer.save()
            return HttpResponse("OK")
        return HttpResponse("FAIL")
    return HttpResponse("FAIL")

class BillingView(NoPermission, generic.ListView):
    model = BillingHeader
    template_name = "facturacion/billingList.html"
    context_object_name = "obj"
    permission_required = "facturacion.view_billingheader"

@login_required(login_url="/login/")
@permission_required("facturacion.change_billingheader", login_url='bases:NoPermission')
def billings(request, id=None):
    template_name = 'facturacion/billings.html'
    detail = {}
    customers = Customer.objects.filter(status=True)
    if request.method == "GET":
        head = BillingHeader.objects.filter(pk=id).first()
        if not head: 
            header = {
                'id': 0,
                'date': datetime.today(),
                'customer':0,
                'subtotal':0.00,
                'discount':0.00,
                'total': 0.00
            }
            detail=None
        else:
            header = {
                'id': head.id,
                'date': head.date,
                'customer':head.customer,
                'subtotal':head.subtotal,
                'discount':head.discount,
                'total': head.total
            }
        detail = BillingDetail.objects.filter(billing=head)
        context = {"head":header, "det":detail, "customers": customers}
        return render(request, template_name, context)

    if request.method == "POST":
        customer = request.POST.get("headerCustomer")
        date = request.POST.get("date")
        custom = Customer.objects.get(pk=customer)
        if not id:
            head = BillingHeader(
                customer = custom,
                date = date,
            )
            if head:
                head.save()
                id = head.id
        else:
            head = BillingHeader.objects.filter(pk=id).first()
            if head:
                head.customer = custom
                head.save()
        if not id:
            messages.error(request, 'Billing Number has not found')
            return redirect("facturacion:billingList")
        code = request.POST.get("code")
        amount = request.POST.get("amount")
        price = request.POST.get("price")
        subtotal = request.POST.get("subtotalDetail")
        discount = request.POST.get("discountDetail")
        total = request.POST.get("totalDetail")
        
        prod = Product.objects.get(code=code)
        det = BillingDetail(
            billing = head,
            product = prod,
            amount = amount,
            price = price,
            subtotal = subtotal,
            discount = discount,
            total = total
        )
        if det:
            det.save()
        return redirect("facturacion:updateBilling", id=id)
    return render(request, template_name, context)

class ProductView(inv.ProductView):
    template_name = "facturacion/searchProduct.html"

def deleteBillingDetail(request, id):
    template_name = "facturacion/deleteBillingDetail.html"
    det = BillingDetail.objects.get(pk=id)
    if request.method == "GET":
        context = {"det":det}
    if request.method == "POST":
        usr = request.POST.get("user") 
        pas = request.POST.get("password")
        user = authenticate(username=usr, password=pas)
        if not user:
            return HttpResponse("Wrong username or password")
        if not user.is_active:
            return HttpResponse("Inactive User")
        if user.is_superuser or user.has_perm("facturas.cashier_supervisor_billingdetail"):
            det.id = None
            det.amount = (-1 * det.amount)
            det.subtotal = (-1 * det.subtotal)
            det.discount = (-1 * det.discount)
            det.total = (-1 * det.total)
            det.save()
            return HttpResponse("ok")
        return HttpResponse("User not allowed")
    return render(request, template_name, context)
    