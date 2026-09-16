from django.forms import ModelForm, TextInput, Textarea, Select

from main.models import Interest


class InterestForm(ModelForm):
    class Meta:
        model = Interest
        fields = ["name", "category", "description"]

        labels = {
            "name": "Interest Name",
            "category": "Category",
            "description": "Description (optional, only for Fun category)",
        }

        widgets = {
            "name": TextInput(attrs={"placeholder": "Web Dev","maxlength": 100}),
            "category": Select(),
            "description": Textarea(attrs={"placeholder": "Tell us about this interest","rows": 3}),
        }