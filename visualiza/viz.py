# -*- coding:utf-8 -*-
"""
Modulo de visualização dos dados do supremo (decisões)
"""
from sqlalchemy import create_engine, MetaData, Table,  func,  join
from sqlalchemy.orm import mapper, sessionmaker
from collections import defaultdict
import cPickle as cp
import time
import cProfile 
import datetime
from lebanco import *

from matplotlib import pyplot as P
import numpy as np
from webviz import blob_map,  annot_TS

#Cria dicionrio de coordenadas dos centroides dos estados
centroides = {}
with open('centroides_estados.csv', 'r') as f:
    for s in f:
        s = s.strip().split(',')
        centroides[s[0]] = (float(s[1]), float(s[2]))

    
def timeit(method):
    """
    Decorator to time methods (or functions)
    """
    def timed(*args, **kw):
        ts = time.time()
        result = method(*args, **kw)
        te = time.time()

        print '%r  %2.2f sec' % \
              (method.__name__ , te-ts)
        return result

    return timed
    
def profileit(fun):
    def timed(*args, **kw):
        result = cProfile(fun(*args, **kw))
        return result

    return timed

class AnalisaCitacoes:
    def __init__(self, session):
        self.session = session

    @timeit
    def calc_freq_lei(self, view=False):
        lei_freq = self.session.query(func.count(Lei.lei), Lei.lei,  Lei.id).group_by(Lei.lei).all()
        freqs = sorted(lei_freq, key=lambda x:x[0],  reverse=True)
    
        def visualiza(freqs):
            freqs = freqs[:20] #top 10
            ind = range(len(freqs))
            alturas = [i[0] for i in freqs]
            xlabels = [i[1] for i in freqs]
            P.bar(ind, alturas,  log=True)
            P.xticks(range(20),xlabels[:20],rotation=45,size='x-small')
            P.title(u'Leis ordenadas por frequência de citação: top 20')
            P.savefig('freq.png')
        if view:
            visualiza(freqs)
        return freqs

    @timeit
    def alcance_temporal(self, view=False):
        """
        Retorna dicionario de decisoes com data da decisao e ano da lei mais antiga citada.
        """
        alc = {}
        for d in self.session.query(Decisao.id, Decisao.data_dec, func.min(Lei.ano)).join((Lei, Decisao.id==Lei.decisao_id)).group_by(Decisao.id).all():
            alc[d[0]] = d[1:]
        def visualiza(alc):
            "histograma"
            P.figure()
            dados=[]
            dados = [i[0].year-i[1] for i in alc.values() if i[1] and i[0]]
            dados  = [d for d in dados if d >0 and d<1000]
            #print dados
            P.hist(dados,  log=True)
            P.title(u'Diferença em anos entre o ano da decisão e o da lei mais antiga citada')
            P.xlabel('Anos')
            P.ylabel(u'Decisões')
            P.savefig('alcance.png')
        if view:
            visualiza(alc)
        return alc
        
    @timeit
    def espacial(self,  view=False):
        """
        generates a blob map with counts decisions by state
        """
        lei_freq = self.session.query(func.count(Decisao), Decisao.data_dec, Decisao.UF).group_by(Decisao.UF).all()
        freqs = sorted(lei_freq, key=lambda x:x[1],  reverse=False)
        data = []
        for p in freqs:
            try:
                data.append((centroides[p[2]][0], centroides[p[2]][1], p[0], p[2]))
            except KeyError:
                pass
#                print p
        mapa = blob_map('Decisoes por estado', 'br', data, 'numero')
        with open('espacial.html', 'w') as f:
            f.write(mapa)
    
    @timeit
    def serie_esferas(self, view=True):
        """
        plota series temporais de citações por esfera
        """
        anodict = defaultdict(lambda:defaultdict(lambda:0))
        leis = self.session.query(Lei.esfera, Lei.id,Lei.lei,  Decisao.data_dec).join((Decisao, Decisao.id==Lei.decisao_id)).all()
        esferas = set([])
        for l in leis:
            if (not l[3]) or l[3].year <1900:
                continue
            anodict[l[3].year][l[0]] += 1
            esferas.add(l[0])
#        print len(leis),anodict.items()[:50]
        t = anodict.keys()
        t.sort()
        series={}
        for e in esferas:
            series[e] = [anodict[i][e] for i in t]
        def visualiza():
            d = np.array(series.values()).T
            P.plot(t, d)
            P.legend(series.keys())
#            P.gca().set_yscale('log')
        html = annot_TS('Serie de citacoes', [datetime.date(i, 12, 31) for i in t], series.values(), series.keys())
        with open('esf_series.html', 'w') as f:
            f.write(html)
        if view:
            visualiza()
            
    @timeit
    def evolucao_sumulas(self, view=True):
        """
        plota series temporais de citações por esfera
        """
        anodict = defaultdict(lambda:0) #contador de citacoes a sumulas
        lfanodict = defaultdict(lambda:0) #contador de leis federais totais
        sumulas = self.session.query(Lei.esfera, Lei.id,Lei.lei,  Decisao.data_dec).join((Decisao, Decisao.id==Lei.decisao_id)).filter(Lei.esfera=='LEG-FED').filter(Lei.lei.like('SUM%')).all()
        leg_fed = self.session.query(Lei.esfera, Decisao.data_dec).join((Decisao, Decisao.id==Lei.decisao_id)).filter(Lei.esfera=='LEG-FED').all()
        # Contagem de sumulas por ano
        for l in sumulas:
            if (not l[3]) or l[3].year <1900:
                continue
            anodict[l[3].year] += 1.
            
        # Contagem de leg-fed por ano
        for l in leg_fed:
            if (not l[1]) or l[1].year <1900:
                continue
            lfanodict[l[1].year] += 1.
            
        # Calcula proporcao
        for a in anodict.keys():
            anodict[a] /=lfanodict[a]

        t = anodict.keys()
        t.sort()
        series={}
        series['Sumula'] = [anodict[ano] for ano in t]
        def visualiza():
            d = np.array(series.values()).T
            P.plot(t, d)
            P.title(u'Citações a súmulas')
            P.xlabel('ano')
            P.ylabel(u'fração do total de citações a legislação federal')
            P.legend(series.keys())
#            P.gca().set_yscale('log')
        html = annot_TS('Decisoes referenciando sumulas', [datetime.date(i, 12, 31) for i in t], series.values(), series.keys())
        with open('evo_sumulas.html', 'w') as f:
            f.write(html)
        if view:
            visualiza()

    @timeit
    def complexidade1(self, view=False):
        """
        calcula indice de complexidade de decisoes como numero de leis citadas
        """
        c = {}
        for d in self.session.query(Decisao.id, func.count(Lei)).join((Lei, Decisao.id==Lei.decisao_id)).group_by(Decisao.id).all():
            c[d[0]] = d[1]
        def visualiza(c):
            "histograma"
            P.figure()
            P.hist(c.values(), log=True)
            P.title(u'Numero de leis citadas por decisão')
            P.xlabel('numero de leis citadas')
            P.ylabel(u'numero de Decisões')
            P.savefig('complexidade.png')
        if view:
            visualiza(c)
        return c

if __name__ == "__main__":
    S = cria_sessao()
#    S.query(Lei).all()
    Ana = AnalisaCitacoes(S)
#    Ana.calc_freq_lei(True)
#    alc = Ana.alcance_temporal(True)
#    Ana.complexidade1(True)


    Ana.espacial(True)
    #Ana.serie_esferas(True)
    Ana.evolucao_sumulas(True)
    P.show()
