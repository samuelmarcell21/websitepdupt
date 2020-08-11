from django.shortcuts import render

def index(request):
    context = {
        'title': 'Halaman Utama',
    }
    return render(request, 'index.html', context)

def find(request):
    return render(request, 'find.html')
