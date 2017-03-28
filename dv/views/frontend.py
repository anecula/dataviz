from django.http import HttpResponse
from django.template.loader import render_to_string


def home(request):
    html = render_to_string('homepage.html')
    return HttpResponse(html)
