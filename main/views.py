from django.contrib import messages
from django.core import serializers
from django.db.models import F
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render

from main.forms import InterestForm
from main.models import Experience, Interest


def show_main(request):
    context = {
        "name": "Aulia Nur Shiva",
        "short_name": "Aulia",
        "npm": "2506619316",
        "study_program": "S1 Information Systems",
        "bio": (
            "Information Systems student at Universitas Indonesia with no idea what my tech career is going to look like yet. I'm currently collecting experiences, trying things that look interesting, and occasionally finding something I actually enjoy. The plan? Figure it out as I go."
        ),
    }
    return render(request, "index.html", context)


def show_experience(request):
    context = {
        "name": "Aulia Nur Shiva",
        "short_name": "Aulia",
        "experience_list": Experience.objects.all().order_by(F("ended_at").desc(nulls_first=True), "-started_at"),
    }
    return render(request, "experience.html", context)

def get_interest_json(request):
    name_query = request.GET.get("name", "").strip()
    interests = Interest.objects.all()

    if name_query:
        interests = interests.filter(name__icontains=name_query)

    interest_json = serializers.serialize("json", interests)
    return HttpResponse(interest_json, content_type="application/json")
  
def show_interest(request):
    json_response = get_interest_json(request)
    interests = serializers.deserialize("json", json_response.content.decode("utf-8"))
    interests = [entry.object for entry in interests]
    name_query = request.GET.get("name", "").strip()

    context = {
        "name": "Aulia Nur Shiva",
        "short_name": "Aulia",
        "exploring_list": [i for i in interests if i.category == "exploring"],
        "fun_list": [i for i in interests if i.category == "fun"],
        "name_query": name_query,
    }
    return render(request, "interest.html", context)
  
def create_interest(request):
    form = InterestForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "New interest added successfully!")
        return redirect("main:show_interest")

    context = {
        "name": "Aulia Nur Shiva",
        "short_name": "Aulia",
        "form": form,
    }
    return render(request, "interest_form.html", context)

def delete_interest(request, interest_id):
    interest = get_object_or_404(Interest, pk=interest_id)

    if request.method == "POST":
        interest.delete()
        messages.success(request, "Interest deleted successfully!")
        return redirect("main:show_interest")

    return redirect("main:show_interest")