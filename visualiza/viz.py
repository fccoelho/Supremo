# -*- coding:utf-8 -*-
"""
Modulo de visualização dos dados do supremo (decisões)
"""
from sqlalchemy import create_engine, MetaData, Table
from sqlalchemy.orm import mapper, sessionmaker
from collections import defaultdict

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
    
def calc_freq_lei(session):
    dq =  session.query(Decisao)
    lei_freq = defaultdict(lambda:0)
    for d in dq:
        lei_freq[tuple(d.legislacao)] += 1
    return lei_freq

if __name__ == "__main__":
    S = loadSession()
#    S.query(Lei).all()
    print calc_freq_lei(S)[:10]
