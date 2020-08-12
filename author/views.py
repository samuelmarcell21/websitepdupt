from django.shortcuts import render
from author.models import Authors
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

# Create your views here.

def showauthor(request):
    result = Authors.objects.all().values('name','nidn','h_index','i10_index')[:100]
    print(result)
    page = request.GET.get('page', 1)
    paginator = Paginator(result, 20)

    try:
        users = paginator.page(page)
    except PageNotAnInteger:
        users = paginator.page(1)
    except EmptyPage:
        users = paginator.page(paginator.num_pages)

    return render(request, 'author/author.html', {'users': users})

def show_detailauthor(request, *args, **kwargs):
    nidn_author = kwargs['nidn']
    author = Authors.objects.filter(nidn=nidn_author).values('name', 'nidn', 'h_index', 'i10_index')
    print(author)

    return render(request, 'author/detail_author.html')