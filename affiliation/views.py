from django.shortcuts import render
from affiliation.models import Affiliations
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from author.models import Authors, Papers

# Create your views here.
def showaffiliation(request):
    if request.method == 'GET':
        univ_list = ['Institut Pertanian Bogor', 'Institut Teknologi Bandung', 'Institut Teknologi Sepuluh Nopember', 'Universitas Airlangga', 'Universitas Diponegoro', 'Unviersitas Gadjah Mada', 'Universitas Hasanuddin', 'Universitas Indonesia', 'Universitas Padjajaran', 'Universitas Pendidikan Indonesia', 'Universitas Sumatera Utara']
        result = Affiliations.objects.filter(name__in=univ_list)
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

        univ_list = ['Institut Pertanian Bogor', 'Institut Teknologi Bandung', 'Institut Teknologi Sepuluh Nopember', 'Universitas Airlangga', 'Universitas Diponegoro', 'Unviersitas Gadjah Mada', 'Universitas Hasanuddin', 'Universitas Indonesia', 'Universitas Padjajaran', 'Universitas Pendidikan Indonesia', 'Universitas Sumatera Utara']
        result = Affiliations.objects.filter(name__in=univ_list).filter(name__icontains=catch)
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
    univ = Affiliations.objects.filter(id_univ=id_univ).first()
    nidn = Authors.objects.filter(univ=id_univ).values('nidn').distinct()
    nidn_fix = []
    for i in nidn:
        nidn_fix.append(i['nidn'])
    paper = Papers.objects.filter(author__in=nidn_fix)[:100]
    # models.Shop.objects.order_by().values('city').distinct()
    page = request.GET.get('page', 1)
    paginator = Paginator(paper, 20)

    try:
        users = paginator.page(page)
    except PageNotAnInteger:
        users = paginator.page(1)
    except EmptyPage:
        users = paginator.page(paginator.num_pages)
    return render(request, 'affiliation/detail_affiliation.html', {'univs': univ, 'users': users})