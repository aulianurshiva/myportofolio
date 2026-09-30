from django.forms import ModelForm, TextInput, Textarea, Select, URLInput, DateTimeInput

from main.models import Interest, Experience
from django.core.exceptions import ValidationError
from django.utils.html import strip_tags

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
    def clean_name(self):
        name = strip_tags(self.cleaned_data["name"]).strip()
        if not name:
            raise ValidationError("Interest name cannot contain only HTML tags.")
        return name

    def clean_description(self):
        return strip_tags(self.cleaned_data["description"]).strip()
    
class ExperienceForm(ModelForm):
    class Meta:
        model = Experience
        fields = ["title","description","thumbnail","started_at","ended_at"]

        labels = {
            "title": "Title",
            "description": "Description",
            "thumbnail": "Thumbnail URL (optional)",
            "started_at": "Start Date",
            "ended_at": "End Date (leave empty if ongoing)"
        }

        widgets = {
            "title": TextInput(attrs={"placeholder": "Teaching Assistant", "maxlength": 255}),
            "description": Textarea(attrs={"placeholder": "Tell us about this experience", "rows": 3}),
            "thumbnail": URLInput(attrs={"placeholder": "https://..."}),
            "started_at": DateTimeInput(attrs={"type": "datetime-local"}, format="%Y-%m-%dT%H:%M"),
            "ended_at": DateTimeInput(attrs={"type": "datetime-local"}, format="%Y-%m-%dT%H:%M"),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["started_at"].input_formats = ["%Y-%m-%dT%H:%M"]
        self.fields["ended_at"].input_formats = ["%Y-%m-%dT%H:%M"]
        self.fields["thumbnail"].required = False
        self.fields["ended_at"].required = False