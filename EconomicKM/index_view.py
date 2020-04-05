from django.shortcuts import render


def index_view(request):
    context={}
    print("index已被访问------------")
    return render(request, 'index.html', context)