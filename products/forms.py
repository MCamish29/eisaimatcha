from django import forms
from .models import Tea, Equipment, Kit, Category, Country

class ProductForm(forms.Form):
    internal_name = forms.CharField(max_length=250)
    product_name = forms.CharField(max_length=250, required=False)
    description = forms.CharField(widget=forms.Textarea)
    blend = forms.CharField(max_length=250, required=False)
    weight = forms.IntegerField(required=False)
    category = forms.ModelChoiceField(queryset=Category.objects.all())
    country_of_origin = forms.ModelChoiceField(queryset=Country.objects.all())
    image = forms.ImageField()
    price = forms.DecimalField(max_digits=10, decimal_places=2)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Set the friendly names for categories using category_id and get_friendly_name
        categories = Category.objects.all()
        friendly_names = [(c.category_id, c.get_friendly_name()) for c in categories]
        self.fields['category'].choices = friendly_names
        
        # Add a class to each field for styling purposes
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'border-black rounded-0'
