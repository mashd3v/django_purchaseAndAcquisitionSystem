from django import forms
from .models import Customer

class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['names', 'lastNames', 'customerType',
                'phone', 'status']
        exclude = ['creationDate', 'modificationDate', 
                'userModifier', 'userCreator']
        widget = {'description': forms.TextInput()}
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class': 'form-control'
            })

