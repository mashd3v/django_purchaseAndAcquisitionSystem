from django import forms
from .models import Category, Subcategory, Brand, MeasurementUnits, Product

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['description', 'status']
        labels = {'description': "Category Description",
        'status': "Status"}
        widget = {'Description': forms.TextInput()}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class': 'form-control'
            })

class SubcategoryForm(forms.ModelForm):
    category = forms.ModelChoiceField(
        queryset = Category.objects.filter(status = True)
        .order_by('description')
    )
    class Meta:
        model = Subcategory
        fields = ['category', 'description', 'status']
        labels = {'description': "Subcategory Description",
            'status': "Status"}
        widget = {'Description': forms.TextInput()}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class': 'form-control'
            })
        self.fields['category'].empty_label = "Choose category"

class BrandForm(forms.ModelForm):
    class Meta:
        model = Brand
        fields = ['description', 'status']
        labels = {'description': "Brand Description",
        'status': "Status"}
        widget = {'Description': forms.TextInput()}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class': 'form-control'
            })

class MeasurementUnitsForm(forms.ModelForm):
    class Meta:
        model = MeasurementUnits
        fields = ['description', 'status']
        labels = {'description': "Measurement Units Description",
        'status': "Status"}
        widget = {'Description': forms.TextInput()}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class': 'form-control'
            })

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['code', 'barCode', 'description', 'status',
                'price', 'stock', 'lastPurchase', 'brand', 
                'subcategory', 'measurementUnits']
        exclude = ['creationDate', 'modificationDate', 'userModifier', 'userCreator']
        widget = {'Description': forms.TextInput()}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class': 'form-control'
            })
        self.fields['lastPurchase'].widget.attrs['readonly'] = True
        self.fields['stock'].widget.attrs['readonly'] = True