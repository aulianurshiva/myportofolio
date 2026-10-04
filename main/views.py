import datetime
from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.db.models import F
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required 
from django.core.exceptions import PermissionDenied        
from main.forms import InterestForm, ExperienceForm
from main.models import Experience, Interest
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.utils import timezone

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
def format_month(value):
    return timezone.localtime(value).strftime("%B %Y")

def get_experience_json(request):
    title_query = request.GET.get("title", "").strip()
    experiences = (
        Experience.objects.prefetch_related("starred_by")
        .order_by(F("ended_at").desc(nulls_first=True), "-started_at")
    )

    if title_query:
        experiences = experiences.filter(title__icontains=title_query)

    data = []
    for experience in experiences:
        starred_users = list(experience.starred_by.all())
        is_starred = request.user in starred_users if request.user.is_authenticated else False

        data.append({
            "pk": str(experience.id),
            "fields": {
                "title": experience.title,
                "description": experience.description,
                "thumbnail": experience.thumbnail or "",
                "started_label": format_month(experience.started_at),
                "ended_label": format_month(experience.ended_at) if experience.ended_at else "Present",
                "is_ongoing": experience.is_ongoing,
                "star_count": len(starred_users),
                "is_starred": is_starred,
                "starred_by_names": ", ".join(u.username for u in starred_users),
            }
        })

    return JsonResponse(data, safe=False)

def show_experience(request):
    context = {
        "name": "Aulia Nur Shiva",
        "short_name": "Aulia",
        "title_query": request.GET.get("title", "").strip(),
        "can_edit": can_edit(request.user),
    }
    return render(request, "experience.html", context)

@login_required(login_url="/login/")
def create_experience(request):
    if not request.user.is_superuser:
        raise PermissionDenied
    
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

@login_required(login_url="/login/")
def update_experience(request, experience_id):
    if not can_edit(request.user):
        raise PermissionDenied
    
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

@login_required(login_url="/login/")
def delete_experience(request, experience_id): 
    if not request.user.is_superuser:
        raise PermissionDenied
    
    experience = get_object_or_404(Experience, pk=experience_id)

    if request.method == "POST":
        experience.delete()
        messages.success(request, "Experience deleted successfully!")
        return redirect("main:show_experience")

    return redirect("main:show_experience")

# === Buat interest ===
def get_interest_json(request):
    name_query = request.GET.get("name", "").strip()
    interests = Interest.objects.prefetch_related("starred_by").order_by("id")

    if name_query:
        interests = interests.filter(name__icontains=name_query)

    data = []
    for interest in interests:
        starred_users = interest.starred_by.all()
        is_starred = request.user in starred_users if request.user.is_authenticated else False
        starred_by_names = ", ".join([u.username for u in starred_users])

        data.append({
            "pk": str(interest.id),
            "fields": {
                "name": interest.name,
                "category": interest.category,
                "description": interest.description,
                "star_count": len(starred_users),
                "is_starred": is_starred,
                "starred_by_names": starred_by_names,
            }
        })

    return JsonResponse(data, safe=False)

def show_interest(request):
    name_query = request.GET.get("name", "").strip()

    context = {
        "name": "Aulia Nur Shiva",
        "short_name": "Aulia",
        "name_query": name_query,
        "form": InterestForm(),
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

@require_POST
def create_interest_ajax(request):
    if not request.user.is_superuser:
        return JsonResponse(
            {"message": "Only the portfolio owner can add interests."},
            status=403,
        )

    form = InterestForm(request.POST)
    if form.is_valid():
        interest = form.save()
        return JsonResponse(
            {"message": "Interest added successfully.", "pk": str(interest.id)},
            status=201,
        )

    return JsonResponse({"errors": form.errors.get_json_data()}, status=400)

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

@login_required(login_url="/login/")
def toggle_star_experience(request, experience_id):
    experience = get_object_or_404(Experience, pk=experience_id)

    if request.method == "POST":
        if request.user in experience.starred_by.all():
            experience.starred_by.remove(request.user)
        else:
            experience.starred_by.add(request.user)

    return redirect("main:show_experience")

def is_editor(user):
    return user.is_authenticated and user.groups.filter(name="Editor").exists()

def can_edit(user):
    return user.is_superuser or is_editor(user)