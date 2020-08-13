from django.shortcuts import render
from .models import Topics
from author.models import Papers

# Create your views here.
def showtopic(request):
    result = Topics.objects.all().values('id_topic','topic_name')
    return render(request, 'topic/topic.html', {'topics': result})

def show_detailtopic(request, *args, **kwargs):
    topic_id = kwargs['id_topic']
    topic = Topics.objects.filter(id_topic=topic_id).values().first()
    paper = Papers.objects.filter(id_topic=topic_id).values('nidn', 'title', 'cite', 'authors', 'year')
    return render(request, 'topic/detail_topic.html', {'topics': topic, 'papers': paper})