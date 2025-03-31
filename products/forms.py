from django import forms
from .models import Tea, Equipment, Kit, Category

class BaseProductForm(forms.ModelForm):
    """ Abstract base form for all product types. """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        categories = Category.objects.all()
        friendly_names = [(c.id, c.get_friendly_name()) for c in categories]

        # Ensure the category field exists before assigning choices
        if 'category' in self.fields:
            self.fields['category'].choices = friendly_names

        # Apply a consistent CSS class to all fields
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'border-black rounded-0'

# Individual forms for each product type
class TeaForm(BaseProductForm):
    class Meta:
        model = Tea
        fields = '__all__'

class EquipmentForm(BaseProductForm):
    class Meta:
        model = Equipment
        fields = '__all__'

class KitForm(BaseProductForm):
    class Meta:
        model = Kit
        fields = '__all__'
