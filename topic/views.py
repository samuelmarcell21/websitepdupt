from django.shortcuts import render
from .models import Topics
from author.models import Papers
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


# Create your views here.
def showtopic(request):
    if request.method == 'GET':
        result = Topics.objects.all().values('id_topic','topic_name')

        page = request.GET.get('page', 1)
        paginator = Paginator(result, 6)

        try:
            users = paginator.page(page)
        except PageNotAnInteger:
            users = paginator.page(1)
        except EmptyPage:
            users = paginator.page(paginator.num_pages)

        return render(request, 'topic/topic.html', {'users': users})

    elif request.method == 'POST':
        catch = request.POST['topic']
        result = Topics.objects.filter(topic_name__icontains=catch).values('id_topic','topic_name')

        page = request.GET.get('page', 1)
        paginator = Paginator(result, 6)

        try:
            users = paginator.page(page)
        except PageNotAnInteger:
            users = paginator.page(1)
        except EmptyPage:
            users = paginator.page(paginator.num_pages)

        return render(request, 'topic/topic.html', {'users': users})

def show_detailtopic(request, *args, **kwargs):
    topic_id = kwargs['id_topic']
    topic = Topics.objects.filter(id_topic=topic_id).values('id_topic').first()
    paper = Papers.objects.filter(id_topic=topic_id).values('nidn', 'title', 'cite', 'authors', 'year', 'id_topic')
    return render(request, 'topic/detail_topic.html', {'topics': topic, 'papers': paper})