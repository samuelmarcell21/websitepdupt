from django.shortcuts import render
from affiliation.models import Affiliations

# Create your views here.
def showaffiliation(request):
    univ_list = ['Institut Pertanian Bogor', 'Institut Teknologi Bandung', 'Institut Teknologi Sepuluh Nopember', 'Universitas Airlangga', 'Universitas Diponegoro', 'Universitas Gadjah Mada', 'Universitas Hasanuddin', 'Universitas Indonesia', 'Universitas Padjajaran', 'Universitas Pendidikan Indonesia', 'Universitas Sumatera Utara']
    result = Affiliations.objects.filter(name__in=univ_list).values('id_univ')
    print(result)
    return render(request, 'affiliation/affiliation.html', {'affiliation':result})