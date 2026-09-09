from django.shortcuts import render

from main.models import Experience


def show_main(request):
    context = {
        "name": "Aulia Nur Shiva",
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
        "experience_list": Experience.objects.all(),
    }
    return render(request, "experience.html", context)