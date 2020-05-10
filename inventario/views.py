from django.shortcuts import render, redirect
from django.views import generic
from .models import Category, Subcategory, Brand, MeasurementUnits, Product
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from .forms import CategoryForm, SubcategoryForm, BrandForm, MeasurementUnitsForm, ProductForm
from django.urls import reverse_lazy
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from bases.views import NoPermission
from django.contrib.auth.decorators import login_required, permission_required
import json

class CategoryView(NoPermission, generic.ListView):
    permission_required = "inventario.view_category"
    model = Category
    template_name = 'inventario/categoryList.html'
    context_object_name = "obj"

class NewCategory(SuccessMessageMixin, NoPermission, generic.CreateView):
    permission_required = "inventario.add_category"
    model = Category
    template_name = "inventario/categoryForm.html"
    context_object_name = "obj"
    form_class = CategoryForm
    success_url = reverse_lazy("inventario:categoryList")
    success_message="Category Successfully Created"
    
    def form_valid(self, form):
        form.instance.userCreator = self.request.user
        return super().form_valid(form)

class UpdateCategory(SuccessMessageMixin, NoPermission, generic.UpdateView):
    permission_required = "inventario.change_category"
    model = Category
    template_name = "inventario/categoryForm.html"
    context_object_name = "obj"
    form_class = CategoryForm
    success_url = reverse_lazy("inventario:categoryList")
    success_message="Category Successfully Updated"
    
    def form_valid(self, form):
        form.instance.userModifier = self.request.user.id
        return super().form_valid(form)

class DeleteCategory(NoPermission, generic.DeleteView):
    permission_required = "inventario.delete_category"
    model = Category
    template_name = 'inventario/deleteCategory.html'
    context_object_name = 'obj'
    success_url = reverse_lazy('inventario:categoryList')

class SubcategoryView(NoPermission, generic.ListView):
    permission_required = "inventario.view_subcategory"
    model = Subcategory
    template_name = 'inventario/subcategoryList.html'
    context_object_name = "obj"

class NewSubcategory(SuccessMessageMixin, NoPermission, generic.CreateView):
    permission_required = "inventario.add_subcategory"
    model = Subcategory
    template_name = "inventario/subcategoryForm.html"
    context_object_name = "obj"
    form_class = SubcategoryForm
    success_url = reverse_lazy("inventario:subcategoryList")
    login_url = "bases:login"
    success_message="Subcategory Successfully Created"
    
    def form_valid(self, form):
        form.instance.userCreator = self.request.user
        return super().form_valid(form)

class UpdateSubcategory(SuccessMessageMixin, NoPermission, generic.UpdateView):
    permission_required = "inventario.change_subcategory"
    model = Subcategory
    template_name = "inventario/subcategoryForm.html"
    context_object_name = "obj"
    form_class = SubcategoryForm
    success_url = reverse_lazy("inventario:subcategoryList")
    login_url = "bases:login"
    success_message="Subcategory Successfully Updated"
    
    def form_valid(self, form):
        form.instance.userModifier = self.request.user.id
        return super().form_valid(form)

class DeleteSubcategory(NoPermission, generic.DeleteView):
    permission_required = "inventario.delete_subcategory"
    model = Subcategory
    template_name = 'inventario/deleteSubcategory.html'
    context_object_name = 'obj'
    success_url = reverse_lazy('inventario:subcategoryList')
    login_url = "bases:login"

class BrandView(NoPermission, generic.ListView):
    permission_required = "inventario.view_brand"
    model = Brand
    template_name = 'inventario/brandList.html'
    context_object_name = "obj"

class NewBrand(SuccessMessageMixin, NoPermission, generic.CreateView):
    permission_required = "inventario.add_brand"
    model = Brand
    template_name = "inventario/brandForm.html"
    context_object_name = "obj"
    form_class = BrandForm
    success_url = reverse_lazy("inventario:brandList")
    login_url = "bases:login"
    success_message="Brand Successfully Created"
    
    def form_valid(self, form):
        form.instance.userCreator = self.request.user
        return super().form_valid(form)

class UpdateBrand(SuccessMessageMixin, NoPermission, generic.UpdateView):
    permission_required = "inventario.change_brand"
    model = Brand
    template_name = "inventario/brandForm.html"
    context_object_name = "obj"
    form_class = BrandForm
    success_url = reverse_lazy("inventario:brandList")
    login_url = "bases:login"
    success_message="Brand Successfully Updated"
    
    def form_valid(self, form):
        form.instance.userModifier = self.request.user.id
        return super().form_valid(form)

@login_required(login_url='/login/')
@permission_required('inventario.change_brand', login_url='bases:noPermission')
def activateBrand(request, id):
    brand = Brand.objects.filter(pk=id).first()
    if not brand:
        return redirect("inventario:brandList")
    if request.method =="GET":
        brand.status = True
        brand.save()
        messages.success(request, 'Brand #' + str(id) + ' Activated')
        return redirect("inventario:brandList")

@login_required(login_url='/login/')
@permission_required('inventario.change_brand', login_url='bases:noPermission')
def deactivateBrand(request, id):
    template_name = 'inventario/deactivateBrand.html'
    context = {}
    brand = Brand.objects.filter(pk=id).first()
    if not brand:
        return HttpResponse('This Brand does not exist: /n Brand #' + str(id))
    if request.method == 'GET':
        context = {'obj': brand}
    if request.method =='POST':
        brand.status = False
        brand.save()
        messages.success(request, 'Brand #' + str(id) + ' Deactivated')
        context = {'obj':'OK'}
        return HttpResponse('Brand deactivated')
    return render(request, template_name, context)

class MeasurementUnitsView(NoPermission, generic.ListView):
    permission_required = "inventario.view_measurementunits"
    model = MeasurementUnits
    template_name = 'inventario/measurementUnitsList.html'
    context_object_name = "obj"

class NewMeasurementUnits(SuccessMessageMixin, NoPermission, generic.CreateView):
    permission_required = "inventario.add_measurementunits"
    model = MeasurementUnits
    template_name = "inventario/measurementUnitsForm.html"
    context_object_name = "obj"
    form_class = MeasurementUnitsForm
    success_url = reverse_lazy("inventario:measurementUnitsList")
    login_url = "bases:login"
    success_message="Unit Of Measurement Successfully Created"
    
    def form_valid(self, form):
        form.instance.userCreator = self.request.user
        return super().form_valid(form)

class UpdateMeasurementUnits(SuccessMessageMixin, NoPermission, generic.UpdateView):
    permission_required = "inventario.change_measurementunits"
    model = MeasurementUnits
    template_name = "inventario/measurementUnitsForm.html"
    context_object_name = "obj"
    form_class = MeasurementUnitsForm
    success_url = reverse_lazy("inventario:measurementUnitsList")
    login_url = "bases:login"
    success_message="Unit Of Measurement Successfully Updated"
    
    def form_valid(self, form):
        form.instance.userModifier = self.request.user.id
        return super().form_valid(form)

@login_required(login_url='/login/')
@permission_required('inventario.change_measurementunits', login_url='bases:noPermission')
def activateMeasurementUnits(request, id):
    mu = MeasurementUnits.objects.filter(pk=id).first()
    if not mu:
        return redirect("inventario:measurementUnitsList")
    if request.method =="GET":
        mu.status = True
        mu.save()
        messages.success(request, 'Unit of Measurement #' + str(id) + ' Activated')
        return redirect("inventario:measurementUnitsList")

@login_required(login_url='/login/')
@permission_required('inventario.change_measurementunits', login_url='bases:noPermission')
def deactivateMeasurementUnits(request, id):
    template_name = 'inventario/deactivateMU.html'
    context = {}
    mu = MeasurementUnits.objects.filter(pk=id).first()
    if not mu:
        return HttpResponse('This Unit of Measurement does not exist: /n Unit of Measurement #' + str(id))
    if request.method == 'GET':
        context = {'obj': mu}
    if request.method =='POST':
        mu.status = False
        mu.save()
        messages.success(request, 'Unit of Measurement #' + str(id) + ' Deactivated')
        context = {'obj':'OK'}
        return HttpResponse('Unit of Measurement deactivated')
    return render(request, template_name, context)

class ProductView(NoPermission, generic.ListView):
    permission_required = "inventario.view_product"
    model = Product
    template_name = 'inventario/productList.html'
    context_object_name = "obj"

class NewProduct(SuccessMessageMixin, NoPermission, generic.CreateView):
    permission_required = "inventario.add_product"
    model = Product
    template_name = "inventario/productForm.html"
    context_object_name = "obj"
    form_class = ProductForm
    success_url = reverse_lazy("inventario:productList")
    login_url = "bases:login"
    success_message="Product Successfully Created"
    
    def form_valid(self, form):
        form.instance.userCreator = self.request.user
        return super().form_valid(form)
    def get_context_data(self, **kwargs):
        context = super(NewProduct, self).get_context_data(**kwargs)
        context["categories"] = Category.objects.all()
        context["subcategories"] = Subcategory.objects.all()
        return context

class UpdateProduct(SuccessMessageMixin, NoPermission, generic.UpdateView):
    permission_required = "inventario.change_product"
    model = Product
    template_name = "inventario/productForm.html"
    context_object_name = "obj"
    form_class = ProductForm
    success_url = reverse_lazy("inventario:productList")
    login_url = "bases:login"
    success_message="Product Successfully Created"
    
    def form_valid(self, form):
        form.instance.userModifier = self.request.user.id
        return super().form_valid(form)
    def get_context_data(self, **kwargs):
        pk = self.kwargs.get('pk')
        context = super(UpdateProduct, self).get_context_data(**kwargs)
        context["categories"] = Category.objects.all()
        context["subcategories"] = Subcategory.objects.all()
        context["obj"] = Product.objects.filter(pk=pk).first()
        return context

@login_required(login_url='/login/')
@permission_required('inventario.change_product', login_url='bases:noPermission')
def activateProduct(request, id):
    product = Product.objects.filter(pk=id).first()
    if not product:
        return redirect("inventario:productList")
    if request.method =="GET":
        product.status = True
        product.save()
        messages.success(request, 'Product #' + str(id) + ' Activated')
        return redirect("inventario:productList")

@login_required(login_url='/login/')
@permission_required('inventario.change_product', login_url='bases:noPermission')
def deactivateProduct(request, id):
    template_name = 'inventario/deactivateProduct.html'
    context = {}
    product = Product.objects.filter(pk=id).first()
    if not product:
        return HttpResponse('This Product does not exist: /n Product #' + str(id))
    if request.method == 'GET':
        context = {'obj': product}
    if request.method =='POST':
        product.status = False
        product.save()
        messages.success(request, 'Product #' + str(id) + ' Deactivated')
        context = {'obj':'OK'}
        return HttpResponse('Product deactivated')
    return render(request, template_name, context)
