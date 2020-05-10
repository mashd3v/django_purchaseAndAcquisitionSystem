from django import forms
from compras.models import Supplier, AcquisitionHeader, AcquisitionDetail

class SupplierForm(forms.ModelForm):
    email = forms.EmailField(max_length=254)
    class Meta:
        model = Supplier
        exclude = ['creationDate', 'modificationDate', 'userModifier', 'userCreator']
        widget = {'Description': forms.TextInput()}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class': 'form-control'
            })
    def clean(self):
        try:
            sc = Supplier.objects.get(
                description = self.cleaned_data["description"].upper()
            )
            if not self.instance.pk:
                raise forms.ValidationError("This register already exist")
            elif self.instance.pk != sc.pk:
                raise forms.ValidationError("Change not permited")
        except Supplier.DoesNotExist:
            pass
        return self.cleaned_data

class AcquisitionHeaderForm(forms.ModelForm):
    aquisitionDate = forms.DateInput()
    billDate = forms.DateInput()
    class Meta:
        model = AcquisitionHeader
        fields = ['supplier', 'acquisitionDate', 'observation',
                'billNumber', 'billDate', 'subtotal', 'discount', 
                'total']
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class': 'form-control'
            })
        self.fields['acquisitionDate'].widget.attrs['readonly'] = True
        self.fields['billDate'].widget.attrs['readonly'] = True
        self.fields['subtotal'].widget.attrs['readonly'] = True
        self.fields['discount'].widget.attrs['readonly'] = True
        self.fields['total'].widget.attrs['readonly'] = True
