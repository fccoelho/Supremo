
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

from matplotlib import pyplot as P

class Lei(object):
    pass
class Decisao(object):
    pass 
class Artigo(object):
    pass 
class Paragrafo(object):
    pass 
class Inciso(object):
    pass 
class Letra(object):
    pass
    
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

def loadSession():
    """faz a conexao com o banco e retorna uma sessao"""
    engine = create_engine("mysql://root:password@E04324/STF_Analise_Decisao", echo=False)
 
    metadata = MetaData(engine)
    decisao = Table('decisao', metadata, autoload=True)
    lei = Table('lei_decisao', metadata, autoload=True)
    artigo = Table('artigo_lei', metadata, autoload=True)
    paragrafo = Table('paragrafo_artigo', metadata, autoload=True)
    inciso = Table('inciso_artigo', metadata, autoload=True)
    letra = Table('letra_inciso', metadata, autoload=True)
    
    mapper(Lei, lei);mapper(Decisao, decisao);mapper(Artigo, artigo);mapper(Paragrafo, paragrafo);mapper(Inciso, inciso);mapper(Letra, letra)
 
    Session = sessionmaker(bind=engine)
    session = Session()
    return session

class AnalisaCitacoes:
    def __init__(self, session):
        self.session = session

    @timeit
    def calc_freq_lei(self, view=False):
        lei_freq = self.session.query(func.count(Lei.lei), Lei.lei,  Lei.id).group_by(Lei.lei).all()
        freqs = sorted(lei_freq, key=lambda x:x[0],  reverse=True)
    
        def visualiza(freqs):
            freqs = freqs[:10] #top 10
            ind = range(len(freqs))
            alturas = [i[0] for i in freqs]
            xlabels = [i[1] for i in freqs]
            P.bar(ind, alturas,  log=True)
            P.xticks(range(10),xlabels[:10],rotation=45,size='x-small')
            P.title(u'Leis ordenadas por frequência de citação: top 10')
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
            P.title('Diferença em anos entre o ano da decisão e o da lei mais antiga citada')
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
            P.title('Numero de leis citadas')
        if view:
            visualiza(c)
        return c

if __name__ == "__main__":
    S = loadSession()
#    S.query(Lei).all()
    Ana = AnalisaCitacoes(S)
    Ana.calc_freq_lei(True)
    alc = Ana.alcance_temporal(True)
    Ana.complexidade1(True)
    P.show()

    

