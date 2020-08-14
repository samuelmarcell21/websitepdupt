from django.shortcuts import render
from affiliation.models import Affiliations
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

# Create your views here.
def showaffiliation(request):
    if request.method == 'GET':
        univ_list = ['Institut Pertanian Bogor', 'Institut Teknologi Bandung', 'Institut Teknologi Sepuluh Nopember', 'Universitas Airlangga', 'Universitas Diponegoro', 'Universitas Gadjah Mada', 'Universitas Hasanuddin', 'Universitas Indonesia', 'Universitas Padjajaran', 'Universitas Pendidikan Indonesia', 'Universitas Sumatera Utara']
        result = Affiliations.objects.filter(name__in=univ_list).values('id_univ', 'name')
        page = request.GET.get('page', 1)
        paginator = Paginator(result, 6)

        try:
            users = paginator.page(page)
        except PageNotAnInteger:
            users = paginator.page(1)
        except EmptyPage:
            users = paginator.page(paginator.num_pages)
        print(result)

        return render(request, 'affiliation/affiliation.html', {'users':users})

    elif request.method == 'POST':
        catch = request.POST['affiliation']

        univ_list = ['Institut Pertanian Bogor', 'Institut Teknologi Bandung', 'Institut Teknologi Sepuluh Nopember', 'Universitas Airlangga', 'Universitas Diponegoro', 'Universitas Gadjah Mada', 'Universitas Hasanuddin', 'Universitas Indonesia', 'Universitas Padjajaran', 'Universitas Pendidikan Indonesia', 'Universitas Sumatera Utara']
        result = Affiliations.objects.filter(name__in=univ_list).filter(name__icontains=catch).values('id_univ', 'name')
        page = request.GET.get('page', 1)
        paginator = Paginator(result, 6)

        try:
            users = paginator.page(page)
        except PageNotAnInteger:
            users = paginator.page(1)
        except EmptyPage:
            users = paginator.page(paginator.num_pages)
        print(result)

        return render(request, 'affiliation/affiliation.html', {'users':users})

def show_detailaffiliation(request, *args, **kwargs):
    id_univ = kwargs['id_univ']
    univ = Affiliations.objects.filter(id_univ=id_univ).values('name')
    return render(request, 'affiliation/detail_affiliation.html', {'univs': univ})