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
    Ana.calc_freq_lei(True)
    alc = Ana.alcance_temporal(True)
    Ana.complexidade1(True)
    P.show()

    

