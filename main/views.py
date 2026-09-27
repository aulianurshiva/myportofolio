import datetime
from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.core import serializers
from django.db.models import F
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required 
from django.core.exceptions import PermissionDenied        
from main.forms import InterestForm, ExperienceForm
from main.models import Experience, Interest


def show_main(request):
    last_login = request.COOKIES.get('last_login', 'No login session yet')
    context = {
        "name": "Aulia Nur Shiva",
        "short_name": "Aulia",
        "npm": "2506619316",
        "study_program": "S1 Information Systems",
        "bio": (
            "Information Systems student at Universitas Indonesia with no idea what my tech career is going to look like yet. I'm currently collecting experiences, trying things that look interesting, and occasionally finding something I actually enjoy. The plan? Figure it out as I go."
        ),
        "last_login": last_login
    }
    return render(request, "index.html", context)

# === Buat experience ===
def get_experience_json(request):
    experiences = Experience.objects.all()
    experience_json = serializers.serialize("json", experiences)
    return HttpResponse(experience_json, content_type="application/json")

def show_experience(request):
    json_response = get_experience_json(request)
    entries = serializers.deserialize("json", json_response.content.decode("utf-8"))
    experience_list = [entry.object for entry in entries]
    experience_list.sort(
        key=lambda e: (
            e.ended_at is not None,
            -(e.started_at.timestamp() if e.started_at else 0),
        )
    )

    context = {
        "name": "Aulia Nur Shiva",
        "short_name": "Aulia",
        "experience_list": Experience.objects.all().order_by(F("ended_at").desc(nulls_first=True), "-started_at"),
    }
    return render(request, "experience.html", context)

def create_experience(request):
    form = ExperienceForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "New experience added successfully!")
        return redirect("main:show_experience")

    context = {
        "name": "Aulia Nur Shiva",
        "short_name": "Aulia",
        "form": form,
        "is_update": False
    }
    return render(request, "experience_form.html", context)

def update_experience(request, experience_id):
    experience = get_object_or_404(Experience, pk=experience_id)
    form = ExperienceForm(request.POST or None, instance=experience)

    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Experience updated successfully!")
        return redirect("main:show_experience")

    context = {
        "name": "Aulia Nur Shiva",
        "short_name": "Aulia",
        "form": form,
        "is_update": True,
    }
    return render(request, "experience_form.html", context)

def delete_experience(request, experience_id): 
    experience = get_object_or_404(Experience, pk=experience_id)

    if request.method == "POST":
        experience.delete()
        messages.success(request, "Experience deleted successfully!")
        return redirect("main:show_experience")

    return redirect("main:show_experience")

# === Buat interest ===
def get_interest_json(request):
    name_query = request.GET.get("name", "").strip()
    interests = Interest.objects.all()

    if name_query:
        interests = interests.filter(name__icontains=name_query)

    interest_json = serializers.serialize("json", interests, use_natural_foreign_keys=True)
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

@login_required(login_url="/login/")  
def create_interest(request):
    if not request.user.is_superuser:
        raise PermissionDenied
    
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

@login_required(login_url="/login/")
def delete_interest(request, interest_id):
    if not request.user.is_superuser:
        raise PermissionDenied

    interest = get_object_or_404(Interest, pk=interest_id)

    if request.method == "POST":
        interest.delete()
        messages.success(request, "Interest deleted successfully!")
        return redirect("main:show_interest")

    return redirect("main:show_interest")

def register(request):
    form = UserCreationForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Account created successfully. Please log in.")
        return redirect("main:login")

    context = {
        "name": "Aulia Nur Shiva",
        "short_name": "Aulia",
        "form": form,
    }

    return render(request, "register.html", context)

def login_user(request):
    form = AuthenticationForm(request, data=request.POST or None)

    if request.method == "POST" and form.is_valid():
        user = form.get_user()
        login(request, user)
        response = redirect("main:show_main")
        response.set_cookie('last_login', datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        return response

    context = {
        "name": "Aulia Nur Shiva",
        "short_name": "Aulia",
        "form": form,
    }

    return render(request, "login.html", context)


def logout_user(request):
    logout(request)
    response = redirect("main:show_main")
    response.delete_cookie('last_login')
    return response

@login_required(login_url="/login/")
def toggle_star_interest(request, interest_id):
    interest = get_object_or_404(Interest, pk=interest_id)

    if request.method == "POST":
        if request.user in interest.starred_by.all():
            interest.starred_by.remove(request.user)
        else:
            interest.starred_by.add(request.user)

    return redirect("main:show_interest")