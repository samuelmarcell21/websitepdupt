from django.shortcuts import render
from author.models import Authors, Papers, Papers_Update, Svg_top
from topic.models import Topics
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Sum
from django.views.generic import View

#SVG
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
import numpy as np
import warnings
warnings.filterwarnings("ignore")
import operator

# Create your views here.

def showauthor(request):
    if request.method == 'GET':
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

    elif request.method == 'POST':
        catch = request.POST['author']
        result = Authors.objects.filter(name__icontains=catch).values('name','nidn','h_index','i10_index')[:100]
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
    author = Authors.objects.get(nidn=nidn_author)
    paper = Papers.objects.filter(nidn=nidn_author).values('nidn', 'title', 'cite', 'authors', 'year')
    sumcite = paper.aggregate(Sum('cite'))
    return render(request, 'author/detail_author.html', {'papers': paper, 'author': author,'countpub':paper.count(),'sumcite':sumcite})

# fungsi svg
#fungsi scaling kolom batas atas
scaler = MinMaxScaler(feature_range=(-1.0, 1.0))
col = ["Topik","Year","xAwalAtas","yAwalAtas","xLengkung1","yLengkung1atas","xLengkung2","yLengkung2atas","xAkhirAtas","yAkhirAtas","xAkhirBawah","yAkhirBawah","yLengkung2bawah","yLengkung1bawah","xAwalBawah","yAwalBawah"]
def fatas(row):
    value = scaler.transform([[row['kumAtas']]])
    return round(float(value),4)

#fungsi scaling kolom batas bawah
def fbawah(row):
    value = scaler.transform([[row['kumBawah']]])
    return round(float(value),4)

def scale_data(data_awal):
    df_scaled=pd.DataFrame()
    
    atas = np.array(data_awal['kumAtas']) #mengambil nilai dari kolom batas atas
    bawah = np.array(data_awal['kumBawah']) #mengambil nilai dari kolom batas bawah
    gabungan = np.append(atas,bawah).reshape(len(bawah)+len(atas),1) # menggabung nilai batas atas dan batas bawah 
    
    #scaling dan proses fit data
    scaler.fit(gabungan)
    
    #transform nilai batas atas dan batas bawah
    data_awal['Scale Atas']=data_awal.apply(fatas,axis=1)
    data_awal['Scale Bawah']=data_awal.apply(fbawah,axis=1)
    
    df_scaled=pd.concat([df_scaled,data_awal])
    
    return df_scaled

class grafik:
    def __init__(self, Topik, Year, scale_atas, scale_bawah, kumAtas, kumBawah,HASIL):
        self.Topik = Topik
        self.Year = Year
        self.xAwalAtas=0
        self.yAwalAtas=0
        self.xLengkung1=0
        self.yLengkung1atas=0
        self.xLengkung2=0
        self.yLengkung2atas=0
        self.xAkhirAtas=0
        self.yAkhirAtas=0
        self.xAkhirBawah=0
        self.yAkhirBawah=0
        self.yLengkung2bawah=0
        self.yLengkung1bawah=0
        self.xAwalBawah=0
        self.yAwalBawah=0
        self.kumAtas=kumAtas
        self.kumBawah=kumBawah
        
        #menghitung titik y
        tahun = self.Year
        topik = self.Topik
        if(tahun==2010):
            self.yAwalAtas=350
            self.yAwalBawah=350
        else:
            self.yAwalAtas=HASIL[(HASIL['Year']==tahun-1) & (HASIL['Topik']==topik)]['yAkhirAtas'].values[0]
            self.yAwalBawah=HASIL[(HASIL['Year']==tahun-1) & (HASIL['Topik']==topik)]['yAkhirBawah'].values[0]
        self.yAkhirAtas = (350 - abs(scale_atas*325))
        if(scale_bawah) > 0:
            self.yAkhirBawah = (350 - abs(scale_bawah*325)) 
        else:
            self.yAkhirBawah = (350 + abs(scale_bawah*325))
            
        #menghitung titik x
        if(tahun==2010):
            self.xAwalAtas=0
            self.xAwalBawah=0
        else:
            self.xAwalAtas=HASIL[(HASIL['Year']==tahun-1) & (HASIL['Topik']==topik)]['xAkhirAtas'].values[0]
            self.xAwalBawah=HASIL[(HASIL['Year']==tahun-1) & (HASIL['Topik']==topik)]['xAkhirBawah'].values[0]
        self.xAkhirAtas = self.xAwalAtas + 150
        self.xAkhirBawah = self.xAwalBawah + 150
    
        #menghitung nilai lengkung
        # xLengkung
        self.xLengkung1 = self.xAwalAtas + 75
        self.xLengkung2 = self.xAkhirAtas - 75

        rangeLengkungAtas = abs(self.yAkhirAtas-self.yAwalAtas)/8
        #yLengkung1atas yang kiri, yLengkung2atas yang kanan  
        self.yLengkung1atas = self.yAwalAtas - rangeLengkungAtas
        self.yLengkung2atas = self.yAkhirAtas + rangeLengkungAtas
        #print(xLengkung1, xLengkung2, rangeLengkung, yLengkung1, yLengkung2)

        rangeLengkungBawah = abs(self.yAkhirBawah-self.yAwalBawah)/8
        # yLengkung1bawah yang kiri, yLengkung2bawah yang kanan
        self.yLengkung1bawah = self.yAwalBawah + rangeLengkungBawah
        self.yLengkung2bawah = self.yAkhirBawah - rangeLengkungBawah
    
    def ubahTitikY(self,yAkhirBawah,yAkhirAtas) :
        self.yAkhirBawah=yAkhirBawah
        self.yAkhirAtas=yAkhirAtas
        
        
        rangeLengkungAtas = abs(self.yAkhirAtas-self.yAwalAtas)/8
        #yLengkung1atas yang kiri, yLengkung2atas yang kanan  
        self.yLengkung1atas = self.yAwalAtas - rangeLengkungAtas
        self.yLengkung2atas = self.yAkhirAtas + rangeLengkungAtas
        #print(xLengkung1, xLengkung2, rangeLengkung, yLengkung1, yLengkung2)

        rangeLengkungBawah = abs(self.yAkhirBawah-self.yAwalBawah)/8
        # yLengkung1bawah yang kiri, yLengkung2bawah yang kanan
        self.yLengkung1bawah = self.yAwalBawah + rangeLengkungBawah
        self.yLengkung2bawah = self.yAkhirBawah - rangeLengkungBawah

    def hasil(self):
        data=[self.Topik,self.Year,self.xAwalAtas,self.yAwalAtas,self.xLengkung1,self.yLengkung1atas,self.xLengkung2,
        self.yLengkung2atas,self.xAkhirAtas,self.yAkhirAtas,self.xAkhirBawah,self.yAkhirBawah,
        self.yLengkung2bawah,self.yLengkung1bawah,self.xAwalBawah,self.yAwalBawah]
        dftmp=pd.DataFrame([data],columns= col)
        return(dftmp)


def Gambar(sorted_listGraf):
    for i in range (len(sorted_listGraf)-1):
#         print('hai')
        new_yAkhirBawah=(sorted_listGraf[i].yAkhirAtas+sorted_listGraf[i].yAkhirBawah) / 2 - 4 # untuk yang diatas
        sorted_listGraf[i].ubahTitikY(new_yAkhirBawah,sorted_listGraf[i].yAkhirAtas) #atas 
        new_yAkhirAtas = sorted_listGraf[i].yAkhirBawah + 4 #untuk yang di bawah 
        sorted_listGraf[i+1].ubahTitikY(sorted_listGraf[i+1].yAkhirBawah,new_yAkhirAtas) #bawah
    return (sorted_listGraf)

def BuatHasil(sorted_listGraf,HASIL):
    for i in sorted_listGraf:
        dftmp=i.hasil()
        HASIL=pd.concat([HASIL,dftmp],axis=0)
    return HASIL


def SVG(request):
    df=pd.DataFrame()
    topik=[1,2,3]
    listdict=[]
    for top in topik:
        obj = Topics.objects.get(id_topic=top)
        data=obj.svg.all().order_by('Year').values()
        temp=pd.DataFrame(data)
        temp2={'name':obj.topic_name}
        listdict.append(temp2)
        # namatopik.append()
        df=pd.concat([df,temp])
    datatopics=Topics.objects.all().values()
    tes=Topics.objects.filter(id_topic=top).values().first()
    data = scale_data(df)#scaling data
    data = data.rename(columns={"id_topic_id": "Topik"})
    # print(data.info())
    data = data.astype({"Topik": float, "Year": float, "kumAtas": float, "kumBawah": float, "batasAtas": float, "batasBawah": float})
    # print(data)
    years=data.Year.unique()
    HASIL = pd.DataFrame(columns=col)
    # print( data[data['Topik']==1])
    for year in years:
        listGraf=[]
        for top in topik:
            a = data[(data['Topik']==top) & (data['Year']==year)]
            # print(a)
            graf=grafik(a['Topik'].values[0],a['Year'].values[0],a['Scale Atas'].values[0],a['Scale Bawah'].values[0],a['kumAtas'].values[0],a['kumBawah'].values[0],HASIL)
            listGraf.append(graf)
        sorted_listGraf = sorted(listGraf, key=operator.attrgetter('kumAtas'), reverse=True)
        sorted_listGraf=Gambar(sorted_listGraf)
        HASIL=BuatHasil(sorted_listGraf,HASIL)
        HASIL=BuatHasil(listGraf,HASIL)
    HASIL['Color']=HASIL.apply(color,axis=1)
    HASIL=HASIL.reset_index(drop=True)
    # print(HASIL.info())
    # print(HASIL)
    data_akhir=HASIL.to_dict('records')

    #Visualisasi samping svg
    dfvis2=df[['id_topic_id','Year','batasAtas']]
    dfvis2 = dfvis2.rename(columns={"id_topic_id": "Topik"})
    dfvis2 = dfvis2.astype({"Topik": float, "Year": float, "batasAtas": float})
    dfvis2= dfvis2[dfvis2['Year']>2017]
    dfvis2['Color']=dfvis2.apply(color,axis=1)
    listvis2=[]
    flag=0
    for top in dfvis2.Topik.unique():
        datay=[]
        for index,row in dfvis2[dfvis2['Topik']==top].iterrows():
            datay.append(row['batasAtas'])
        data={'x':listdict[flag]['name'],'y':datay,'Color':row['Color']}
        flag+=1
        listvis2.append(data)
    print(datatopics)
    
    return render(request, 'author/SVG.html',{'data':data_akhir,'nama_top':listdict,'data2':listvis2,'datatopics':datatopics})


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
        va='#cef397'
    elif(row['Topik']==14):
        val=='#22875c'        
    elif(row['Topik']==15):
        val=='#a3c6ae'       
    elif(row['Topik']==16):
        val=='#d15ac9'       
    elif(row['Topik']==17):
        val=='#7758fb'       
    elif(row['Topik']==18):
        val=='#63b9c8'       
    return val



class AjaxHandlerView(View):
    def get(self,request):
        text = request.GET.get('button_text')
        print(text)
        datatopics=Topics.objects.all().values()

        return render(request, 'author/cobajax.html',{'datatopics':datatopics})


