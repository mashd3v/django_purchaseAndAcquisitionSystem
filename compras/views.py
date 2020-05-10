from django.shortcuts import render, redirect
from django.views import generic
from .models import Supplier, AcquisitionDetail, AcquisitionHeader
from inventario.models import Product
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse, JsonResponse
import json
import datetime
from compras.forms import SupplierForm, AcquisitionHeaderForm
from django.urls import reverse_lazy
from bases.views import NoPermission
from django.contrib import messages
from django.db.models import Sum
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.decorators import login_required, permission_required

class SupplierView(NoPermission, generic.ListView):
    permission_required = "compras.view_supplier"
    model = Supplier
    template_name = 'compras/supplierList.html'
    context_object_name = "obj"

class NewSupplier(SuccessMessageMixin, NoPermission, generic.CreateView):
    permission_required = "compras.add_supplier"
    model = Supplier
    template_name = "compras/supplierForm.html"
    context_object_name = "obj"
    form_class = SupplierForm
    success_url = reverse_lazy("compras:supplierList")
    login_url = "bases:login"
    success_message="Supplier Successfully Created"
    
    def form_valid(self, form):
        form.instance.userCreator = self.request.user
        return super().form_valid(form)

class UpdateSupplier(SuccessMessageMixin, NoPermission, generic.UpdateView):
    permission_required = "compras.change_supplier"
    model = Supplier
    template_name = "compras/supplierForm.html"
    context_object_name = "obj"
    form_class = SupplierForm
    success_url = reverse_lazy("compras:supplierList")
    login_url = "bases:login"
    success_message="Supplier Successfully Updated"
    
    def form_valid(self, form):
        form.instance.userModifier = self.request.user.id
        return super().form_valid(form)

@login_required(login_url='/login/')
@permission_required('compras.change_supplier', login_url='bases:noPermission')
def deactivateSuppliers(request, id):
    template_name = 'compras/deactivateSuppliers.html'
    context = {}
    supplier = Supplier.objects.filter(pk=id).first()
    if not supplier:
        return HttpResponse('This supplier does not exist: /n Supplier #' + str(id))
    if request.method == 'GET':
        context = {'obj': supplier}
    if request.method =='POST':
        supplier.status = False
        supplier.save()
        messages.success(request, 'Supplier #' + str(id) + ' Deactivated')
        context = {'obj':'OK'}
        return HttpResponse('Supplier deactivated')
    return render(request, template_name, context)

class AcquisitionView(NoPermission, generic.ListView):
    permission_required = "compras.view_acquisitionheader"
    model = AcquisitionHeader
    template_name = 'compras/acquisitionList.html'
    context_object_name = "obj"

@login_required(login_url='/login/')
@permission_required('compras.view_acquisitionheader', login_url='bases:noPermission')
def acquisition(request, acquisition_id=None):
    template_name = "compras/acquisition.html"
    product = Product.objects.filter(status=True)
    form_acquisition = {}
    context = {}
    if request.method =='GET':
        form_acquisition = AcquisitionHeaderForm()
        header = AcquisitionHeader.objects.filter(pk = acquisition_id).first()
        if header:
            detail = AcquisitionDetail.objects.filter(acquisition = header)
            acquisitionDate = datetime.date.isoformat(header.acquisitionDate)
            billDate = datetime.date.isoformat(header.billDate)
            e = {
                'acquisitionDate': acquisitionDate,
                'supplier': header.supplier,
                'observation': header.observation,
                'billNumber': header.billNumber,
                'billDate': billDate,
                'subtotal': header.subtotal,
                'discount': header.discount,
                'total': header.total,
            }
            form_acquisition = AcquisitionHeaderForm(e)
        else:
            detail = None
        context = {'products': product,
                    'header': header,
                    'detail': detail,
                    'form_header': form_acquisition,}
    if request.method == 'POST':
        acquisitionDate = request.POST.get("acquisitionDate")
        observation = request.POST.get("observation")
        billNumber = request.POST.get("billNumber")
        billDate = request.POST.get("billDate")
        supplier = request.POST.get("supplier")
        subtotal = 0
        discount = 0
        total = 0
        if not acquisition_id:
            supplier = Supplier.objects.get(pk = supplier)
            header = AcquisitionHeader(
                acquisitionDate = acquisitionDate,
                observation = observation,
                billNumber = billNumber,
                billDate = billDate,
                supplier = supplier,
                userCreator = request.user
            )
            if header:
                header.save()
                acquisition_id = header.id
        else:
            header = AcquisitionHeader.objects.filter(pk = acquisition_id).first()
            if header:
                header.acquisitionDate = acquisitionDate
                header.observation = observation
                header.billNumber = billNumber
                header.billDate = billDate
                header.userModifier = request.user.id
                header.save()
        if not acquisition_id:
            return redirect("compras:acquisitionList")
        product = request.POST.get("id_id_product")
        amount = request.POST.get("id_amount_detail")
        price = request.POST.get("id_price_detail")
        subtotalDetail = request.POST.get("id_subtotal_detail")
        discountDetail = request.POST.get("id_discount_detail")
        totalDetail = request.POST.get("id_total_detail")
        product = Product.objects.get(pk = product)
        detail = AcquisitionDetail(
            acquisition = header,
            product = product,
            amount = amount,
            supplierPrice = price,
            discount = discountDetail,
            cost = 0,
            userCreator = request.user
        )
        if detail:
            detail.save()
            subtotal = AcquisitionDetail.objects.filter(acquisition = acquisition_id).aggregate(Sum('subtotal'))
            discount = AcquisitionDetail.objects.filter(acquisition = acquisition_id).aggregate(Sum('discount'))
            header.subtotal = subtotal["subtotal__sum"]
            header.discount = discount["discount__sum"]
            header.save()
        return redirect("compras:updateAcquisition", acquisition_id = acquisition_id)
    return render(request, template_name, context)

class AcquisitionDetailDelete(NoPermission, generic.DeleteView):
    permission_required = "compras.delete_acquisitiondetail"
    model = AcquisitionDetail
    template_name = "compras/acquisitionDetailDelete.html"
    context_object_name = 'obj'
    def get_success_url(self):
        acquisition_id = self.kwargs['acquisition_id']
        return reverse_lazy('compras:updateAcquisition', kwargs = {'acquisition_id': acquisition_id})