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
        self.freqs = self.calc_freq_lei(session)

    @timeit
    def calc_freq_lei(self, session):
        lei_freq = session.query(func.count(Lei.lei), Lei.lei,  Lei.id).group_by(Lei.lei).all()
        return sorted(lei_freq, key=lambda x:x[0],  reverse=True)
    
    def visualiza_freq_lei(self, freqs):
        freqs = freqs[:100] #top 100
        ind = range(len(freqs))
        alturas = [i[0] for i in freqs]
        xlabels = [i[1] for i in freqs]
        P.bar(ind, alturas,  log=True)
        P.show()
    
    @timeit
    def alcance_temporal(self):
        """
        Retorna dicionario de decisoes co data da decisao e ano da lei mais antiga citada.
        """
        alc = {}
        for d in self.session.query(Decisao.id, Decisao.data_dec, func.min(Lei.ano)).join((Lei, Decisao.id==Lei.decisao_id)).group_by(Decisao.id).all():
            alc[d[0]] = d[1:]
            
        return alc
    


if __name__ == "__main__":
    S = loadSession()
#    S.query(Lei).all()
    Ana = AnalisaCitacoes(S)
#    Ana.visualiza_freq_lei(Ana.freqs)
    alc = Ana.alcance_temporal()
    print len(Ana.freqs)

    

