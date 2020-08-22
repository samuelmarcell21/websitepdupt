from django.shortcuts import render
from django.http import HttpResponseRedirect

from author.models import Papers, Authors
from topic.models import Topics
from affiliation.models import Affiliations


# Untuk Search
import re
import numpy as np
import pandas as pd
from pprint import pprint

from Sastrawi.Stemmer.StemmerFactory import StemmerFactory

# Gensim

from gensim.corpora import Dictionary
from gensim.corpora.mmcorpus import MmCorpus
import gensim
import gensim.corpora as corpora
from gensim.utils import simple_preprocess
from gensim.models import CoherenceModel
from nltk.corpus import stopwords

# spacy for lemmatization
import spacy

# Plotting tools
import pyLDAvis
import pyLDAvis.gensim  # don't skip this
import matplotlib.pyplot as plt

# Enable logging for gensim - optional
import logging
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.ERROR)

import warnings
warnings.filterwarnings("ignore",category=DeprecationWarning)
import pandas as pd

from django.views.generic import ListView

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from gensim.similarities import MatrixSimilarity

from gensim.models import TfidfModel
from gensim.matutils import cossim as CS

import pickle
from gensim.similarities.docsim import Similarity
from gensim.test.utils import get_tmpfile
import gensim
from IPython.display import clear_output

global color

def svg(total_pub_topic1, total_pub_topic2, total_pub_topic3, total_pub_topic4, total_pub_topic5, i):
    color = ['green', 'yellow', 'red', 'blue', 'lime']
    jarak_topic1 = (total_pub_topic1/3000)*120
    jarak_topic2 = (total_pub_topic2/3000)*120
    jarak_topic3 = (total_pub_topic3/3000)*120
    jarak_topic4 = (total_pub_topic4/3000)*120
    jarak_topic5 = (total_pub_topic5/3000)*120
    x_topic1 = 300
    y_topic1 = 200-jarak_topic1
    x_topic2 = 300 + ((416-300)*(jarak_topic2/120))
    y_topic2 = 200 - ((200-157)*(jarak_topic2/120))
    x_topic3 = 300 + ((382-300)*(jarak_topic3/120))
    y_topic3 = 200 + ((302-200)*(jarak_topic3/120))
    x_topic4 = 300 - ((300-233)*(jarak_topic4/120))
    y_topic4 = 200 + ((302-200)*(jarak_topic4/120))
    x_topic5 = 300 - ((300-198)*(jarak_topic5/120))
    y_topic5 = 200 - ((200-157)*(jarak_topic5/120))
    print('''
<polygon points="{},{} {},{} {},{} {},{} {},{}" style="fill:{}; fill-opacity:0.5;stroke:{};stroke-width:3" />
<circle cx="{}" cy="{}" r="2" stroke="black" stroke-width="1" fill-opacity='1' />
<circle cx="{}" cy="{}" r="2" stroke="black" stroke-width="1" fill-opacity='1' />
<circle cx="{}" cy="{}" r="2" stroke="black" stroke-width="1" fill-opacity='1' />
<circle cx="{}" cy="{}" r="2" stroke="black" stroke-width="1" fill-opacity='1' />
<circle cx="{}" cy="{}" r="2" stroke="black" stroke-width="1" fill-opacity='1' />
    '''.format(x_topic1, y_topic1, x_topic2, y_topic2, x_topic3, y_topic3, x_topic4, y_topic4, x_topic5, y_topic5, color[i] , color[i], x_topic1, y_topic1, x_topic2, y_topic2, x_topic3, y_topic3, x_topic4, y_topic4, x_topic5, y_topic5))

def index(request):
    context = {
        'title': 'Halaman Utama',
    }
    return render(request, 'index.html', context)

def find(request):
    topic = Topics.objects.all().order_by('-total_publication')[:5]
    for i in topic:
        print(i.topic_name)
    affiliation = Affiliations.objects.all().order_by('-total_publication')[:5]
    univ = []
    for i in affiliation:
        univ.append(i.initial_univ)
    # print(univ)
    # univ = []
    # arr_peruniv = []
    # for i in affiliation:
    #     arr_peruniv.append(i.id_univ)
    #     researcher = Authors.objects.filter(univ=i.id_univ)
    #     for b in topic:
    #         count = 0
    #         for a in researcher:
    #             paper = Papers.objects.filter(author = a.nidn, topic=b.id_topic)
    #             count += len(paper)
    #         arr_peruniv.append(count)   
    #     univ.append(arr_peruniv)

    arr_visualisasi = [['6', 1826, 2477, 852, 1535, 1408], ['1', 552, 1797, 665, 2176, 714], ['8', 1802, 335, 1660, 709, 506], ['5', 816, 1346, 801, 771, 1723], ['2', 1598, 288, 762, 939, 286]]
    arr_svg = []
    for i in range(len(arr_visualisasi)):
        arr_svg.append(svg(arr_visualisasi[i][1], arr_visualisasi[i][2], arr_visualisasi[i][3], arr_visualisasi[i][4], arr_visualisasi[i][5], i))
    # print(univ)
    # print(arr_svg)
    return render(request, 'find.html', {'arr_svg': arr_svg})

def search(request):
    if request.method == 'POST':
        catch = request.POST['title']
        data = [catch]
        
        stop_words = stopwords.words('indonesian')
        stop_words2 = stopwords.words('english')
        stop_words.extend(stop_words2)
        stop_words.extend(['of','in','and','the','for','on','using','based','from','with','to','by','as','an','pengaruh'
                        ,'effect','analisis','at','pre','pro','analysis','berbasis','tahun','between','kualitas','method',
                        'metode','through','menggunakan','hasil'])
        
        # Remove Numbers
        data = [re.sub(" \d+",' ', sent) for sent in data]
        data = [re.sub('[^a-zA-Z]',' ', sent) for sent in data]

        # Remove new line characters
        data = [re.sub('\s+', ' ', sent) for sent in data]

        # Remove distracting single quotes
        data = [re.sub("\'", "", sent) for sent in data]

        def sent_to_words(sentences):
            for sentence in sentences:
                yield(gensim.utils.simple_preprocess(str(sentence), deacc=True))  # deacc=True removes punctuations

        coba = sent_to_words(data)
        data_words = list(coba)

        # Build the bigram and trigram models
        bigram = gensim.models.Phrases(data_words, min_count=5, threshold=100) # higher threshold fewer phrases.
        trigram = gensim.models.Phrases(bigram[data_words], threshold=100)  

        # Faster way to get a sentence clubbed as a trigram/bigram
        bigram_mod = gensim.models.phrases.Phraser(bigram)
        trigram_mod = gensim.models.phrases.Phraser(trigram)

        # Define functions for stopwords, bigrams, trigrams and lemmatization
        # from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
        def remove_stopwords(texts):
            return [[word for word in simple_preprocess(str(doc)) if word not in (stop_words or stop_words2)] for doc in texts]

        def make_bigrams(texts):
            return [bigram_mod[doc] for doc in texts]

        def make_trigrams(texts):
            return [trigram_mod[bigram_mod[doc]] for doc in texts]

        def lemmatization(texts):
            """https://spacy.io/api/annotation"""
            texts_out = []
            for sent in texts:
                doc = nlp(" ".join(sent)) 
                texts_out.append([token.lemma_ for token in doc])
            return texts_out

        # Remove Stop Words
        data_words_nostops = remove_stopwords(data_words)

        # # Form Bigrams
        data_words_bigrams = make_bigrams(data_words_nostops)

        nlp = spacy.load('en_core_web_sm')

        data_lemmatized = lemmatization(data_words_bigrams)

        #stem masing-masing kata yang ada
        factory = StemmerFactory()
        stemmer = factory.create_stemmer()

        for x in range(len(data_lemmatized)-1):
            for y in range(len(data_lemmatized[x])-1):
                data_lemmatized[x][y] = stemmer.stem(data_lemmatized[x][y])

        id2wordd = corpora.Dictionary(data_lemmatized)
        # Create Corpus
        texts = data_lemmatized
        # Term Document Frequency
        corpuss = [id2wordd.doc2bow(text) for text in texts]

        id2word = Dictionary.load('websitepdupt/id2word_new.dict')
        corpus = MmCorpus('websitepdupt/corpus_new.mm')

        # import gensim
        model = gensim.models.ldamodel.LdaModel.load('websitepdupt/mallet_18_lda.mdl', mmap='r') 
        new_doc_bow = id2word.doc2bow(data_lemmatized[0])
        hasil = model.get_document_topics(new_doc_bow)

        topic=0
        nilai =-99
        for i, row in (hasil):
            if(row>nilai):
                topic=i
                nilai=row
        
        keywords=[]
        
        for i,nilai in model.show_topic(topic):
            keywords.append(i)

        # topics = Topics.objects.filter(id_topic=topic).values_list('id_publication', flat=True)

        #load data
        df = pd.read_csv('websitepdupt/label18baru.csv')
        with open("websitepdupt/lemma_new.txt", "rb") as fp:   #Pickling
            data_lemmatizedd=pickle.load(fp)

        #init tempat menyimpan hasil
        hasil_cosine_keseluruhan=[]
        hasil_cosine=[]

        #mengambil data yang sesuai dengan topik
        # topic=df
        topik=df.loc[df['Topic1'] == topic]

        ##membuat data lemma, corpus dan dictionary berdasarkan data dalam 1 topik
        res_list = [data_lemmatizedd[i] for i in topik.index] 
        # Create Dictionary
        id2worddd = corpora.Dictionary(res_list)

        # Create Corpus
        texts = res_list

        # Term Document Frequency
        corpusss = [id2worddd.doc2bow(text) for text in res_list]

        #menghitung cosine sim judul dibandingkan dengan keseluruhan judul yang ada

        index_tmpfile = get_tmpfile("index")
        index = Similarity(index_tmpfile,corpusss, num_features=len(id2worddd))

        index = MatrixSimilarity(corpusss, num_features=len(id2worddd))
        sims = index[corpuss]

        sort_index = np.argsort(sims[0])

        reversed_arr = sort_index[::-1]

        hasil = pd.DataFrame(reversed_arr)

        hasilbaru = hasil.iloc[:40,:]

        hasilmantep = hasilbaru.to_numpy()

        idfix=[]
        for i in range(0,40):
            idfix.append(hasilmantep[i][0])

        ngetest = topik.to_numpy()

        id_artikel = []
        for i in idfix:
            id_artikel.append(ngetest[i][9])

        # global user_list
        user_list = Papers.objects.filter(id_pub__in=id_artikel).order_by('id_pub').values('title', 'cite', 'authors', 'year', 'id_topic')

        # global hasiltopik
        # hasiltopik = topic_dict.get(str(topic))

        topic_obj = Topics.objects.filter(id_topic=topic+1).values('topic_name')

        page = request.GET.get('page', 1)
        paginator = Paginator(user_list, 10)

        try:
            users = paginator.page(page)
        except PageNotAnInteger:
            users = paginator.page(1)
        except EmptyPage:
            users = paginator.page(paginator.num_pages)
        
        context = {
            'title': 'Halaman Utama',
            'topik': topic_obj,
            'catch': catch,
            'users' : users,
        }

        return render(request, 'search.html', context)
