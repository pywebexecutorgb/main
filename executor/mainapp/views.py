from django.shortcuts import render
from django.urls import reverse
from django.views.generic import DetailView, CreateView

activity_buttons = [
{
    'href': 'index', 'name': 'run'
},
{
    'href': 'index', 'name': 'save'
},
{
    'href': 'index', 'name': 'new'
},
]

def main(request):
    title = 'WebExecutor'
    content = {
        'title': title,
        'activity_buttons': activity_buttons,
    }

    return render(request, 'mainapp/index.html', content)
