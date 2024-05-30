from django.shortcuts import render

from pathlib import Path
BASE_DIR = Path(__file__).resolve().parent.parent


def home(request):
    context = {}
    return render(request, BASE_DIR / 'templates/home.html', context)
