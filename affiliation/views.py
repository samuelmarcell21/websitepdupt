from django.shortcuts import render
from affiliation.models import Affiliations
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from author.models import Authors, Papers
import pandas as pd
import numpy as np
from django.db.models import Sum
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
    list_count,list_sum=vis_affil(id_univ)
    return render(request, 'affiliation/detail_affiliation.html', {'univs': univ, 'users': users,'data_count':list_count,'data_sum':list_sum})


def color(row):
    if(row['Topik']==0):
        val='#2d97ab'
    elif(row['Topik']==1):
        val='#ed164f'
    elif(row['Topik']==2):
        val='#72801b'
    elif(row['Topik']==3):
        val='#755e5c'
    elif(row['Topik']==4):
        val='#e9ce86'
    elif(row['Topik']==5):
        val='#8851d2'
    elif(row['Topik']==6):
        val='#ccbd73'
    elif(row['Topik']==7):
        val='#7acdd3'
    elif(row['Topik']==8):
        val='#7254da'
    elif(row['Topik']==9):
        val='#655e2d'
    elif(row['Topik']==10):
        val='#75377d'
    elif(row['Topik']==11):
        val='#bea56b'
    elif(row['Topik']==12):
        val='#e18a39'
    elif(row['Topik']==13):
        val='#cef397'
    elif(row['Topik']==14):
        val='#22875c'        
    elif(row['Topik']==15):
        val='#a3c6ae'       
    elif(row['Topik']==16):
        val='#d15ac9'       
    elif(row['Topik']==17):
        val='#7758fb'       
    elif(row['Topik']==18):
        val='#63b9c8'       
    return val

def vis_affil(id_univ):
    univ= Affiliations.objects.get(id_univ=id_univ)
    YEAR=['2010','2011','2012','2013','2014','2015','2016','2017','2018','2019','2020']
    TOPIK=[univ.topik_dominan1_id,univ.topik_dominan2_id,univ.topik_dominan3_id]
    TOPIK_NAMA=[univ.topik_dominan1.topic_name,univ.topik_dominan2.topic_name,univ.topik_dominan3.topic_name]
    # print(dir(univ.aut))
    # print(univ.aut.paper)
    df=pd.DataFrame(columns=['Topic','Year','Count','Sumcite'])
    df['Topic']=[TOPIK[0]]*11 + [TOPIK[1]]*11 + [TOPIK[2]]*11
    df['Year']=(YEAR)*3
    df = df.astype({"Topic": int,"Year": int})
    # flag=0
    df['Count']=0
    df['Sumcite']=0
    for aut in univ.aut.all():
        # print(flag,'/',univ.aut.count())
        # flag +=1
        for top in TOPIK:
            papers_top = aut.paper.filter(topic_id=top)
            year_dis = papers_top.values('year').distinct()
            for year in year_dis:
                cou=papers_top.filter(year=year['year']).count()
                sumc=papers_top.filter(year=year['year']).aggregate(Sum('cite'))['cite__sum']
                if(sumc is None):
                    sumc=0
                df.loc[(df["Topic"] == int(top)) & (df["Year"] == int(year['year'])), "Count"] += cou
                df.loc[(df["Topic"] == int(top)) & (df["Year"] == int(year['year'])), "Sumcite"] += sumc
    df = df.rename(columns={"Topic": "Topik"})
    df = df.astype({"Topik": int})
    df['Color']=df.apply(color,axis=1)
    flag=0
    list_count=[]
    list_sum=[]
    for top in df.Topik.unique():
        datacount=[]
        datasum=[]
        for index,row in df[df['Topik']==top].iterrows():
            datacount.append(row['Count'])
            datasum.append(row['Sumcite'])
        datac={'x':TOPIK_NAMA[flag],'y':datacount,'Color':row['Color']}
        datas={'x':TOPIK_NAMA[flag],'y':datasum,'Color':row['Color']}
        flag+=1
        list_count.append(datac)
        list_sum.append(datas)     
    print(list_count)
    print(list_sum)           
    return(list_count,list_sum)