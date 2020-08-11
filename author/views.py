from django.shortcuts import render
from author.models import Authors

# Create your views here.

def showauthor(request):
    result = Authors.objects.all().values('name','nidn','h_index','i10_index')
    # print(result)
    return render(request, 'author/author.html', {'author':result})