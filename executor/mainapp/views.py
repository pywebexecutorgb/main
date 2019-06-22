from django.shortcuts import render

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
