from . fuzzyset import compile
from django.shortcuts import render


def home(request):
    content = compile()
    chart = content['quality_of_service_graph']
    return render(request, 'index.html', {'chart': chart})

