from django.shortcuts import render

links_main_menu = [
{
    'href': '#', 'name': 'Запустить'
},
{
    'href': '#', 'name': 'Сохранить'
},
]

def toolbar_menu(request):
    title = 'PyExecutor'
    content = {
        'title': title,
        'links_main_menu': links_main_menu,
    }

    return render(request, 'mainapp/index.html', content)
