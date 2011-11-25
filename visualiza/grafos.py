# -*- coding:utf-8 -*-
'''
Created on 05/04/2011

@author: flavio
'''


import networkx as nx
from networkx import NetworkXError
import os
import time
from itertools import cycle
from sqlalchemy.ext.sqlsoup import SqlSoup
import numpy as np
import matplotlib.pyplot as P
from matplotlib.colors import rgb2hex
from matplotlib import cm
import ubigraph
import cPickle
import gzip
import getpass
import MySQLdb
from MySQLdb.cursors import CursorUseResultMixIn,  DictCursor, SSDictCursor, SSCursor
'''
Configurações:
'''
confs = "Flavio"

if confs == "Flavio":
    dbgrafo =MySQLdb.connect(host="10.251.1.137", user="root", passwd="mysqlFGV13",db="SEN_Grafo")
    dbdec =MySQLdb.connect(host="10.251.1.137", user="root", passwd="mysqlFGV13",db="STF_Analise_Decisao")
    curgrafo=dbgrafo.cursor(cursorclass=SSCursor)
    curdec=dbdec.cursor(cursorclass=SSCursor)
#    passw = getpass.getpass("Senha do MySQL:")
    ubiServer = "http://127.0.0.1:20738/RPC2"
#    MySQLServer = "mysql://root:passw@10.251.1.137"

if confs == "Pablo":
    ubiServer = "http://127.0.0.1:20738/RPC2"
    MySQLServer = "mysql://pablo:pablo@10.251.1.137"

'''
Final das configurações
'''

cf88_vs_outras_q = """
select 
  1 lei_id_1, ld_1.lei_id lei_id_2, count(ld_1.lei_id) peso
from 
  lei_decisao ld_1
where 
  ld_1.decisao_id in (
    select 
      ld_2.decisao_id
    from
      lei_decisao ld_2
    where
      ld_2.lei_id = 1
  ) and
  ld_1.lei_id <> 1
group by
  ld_1.lei_id
order by
  count(ld_1.lei_id) desc
"""

def timeit(fun):
    """
    Decorator to time methods (or functions)
    """
    def timed(*args, **kw):
        ts = time.time()
        result = fun(*args, **kw)
        te = time.time()
        print '%r (%s,%s)  %2.2f sec'%(fun.__name__, args, kw , te-ts)
        return result
    return timed

def dyn_graph_general(elist, order, vstyles=[],estyles=[]):
    """
    Visualização dinâmica usando ubigraph
    Servidor Ubigraph deve estar rodando na URL indicada
    elist is a list of tuples: (n1,n2,w)
    """
    U = ubigraph.Ubigraph(URL=ubiServer)
    U.clear()
    nodes = {}
    edges = set([])
    maxw = float(max(np.array([i[2] for i in elist]))) #largest weight
    if not vstyles:
        vstyles = cycle([U.newVertexStyle(id=1,shape="sphere", color="#ff0000")])
    else:
        vstyles = cycle(vstyles)

    lei_style = U.newVertexStyle(id=2,shape="sphere", color="#00ff00")

    for e in elist:
        if e[0] not in nodes:
            n1 = U.newVertex(style=vstyles.next(), label=str(e[0]).decode('latin-1'))
            nodes[e[0]] = n1
        else:
            n1 = nodes[e[0]]
        if e[1] not in nodes:
            n2 = U.newVertex(style=lei_style, label=str(e[1]))
            nodes[e[1]] = n2
        else:
            n2 = nodes[e[1]]
        es = e[2]/maxw
        if (n1,n2) not in edges:
            U.newEdge(n1,n2,spline=True,strength=es, width=2.0, showstrain=True)
            edges.add((n1,n2))
            edges.add((n2,n1))

def dyn_graph_lei(elist):
    """
    Visualização dinâmica usando ubigraph
    Servidor Ubigraph deve estar rodando na URL indicada
    """
    U = ubigraph.Ubigraph(URL=ubiServer)
    U.clear()
    ''' Versão 1 '''
    v_styles = {'LEG-FED':U.newVertexStyle(id=1,shape="cube", color="#ff0000"),
                'LEG-EST':U.newVertexStyle(id=2,shape="cube", color="#00ff00"),
                'LEG-MUN':U.newVertexStyle(id=3,shape="cube", color="#0000ff"),
                'LEG-DIS':U.newVertexStyle(id=4,shape="cube", color="#0ff000"),
                'LEG-INT':U.newVertexStyle(id=5,shape="cube", color="#000ff0"),
                'outras':U.newVertexStyle(id=6,shape="cube", color="#f0f000"),
                'CF':U.newVertexStyle(id=6,shape="cube", color="#00ff00"),
                }
    
    ''' Versão 2 
    v_styles = {'CF':U.newVertexStyle(id=1,shape="sphere", color="#ff0000"),
                'LEI':U.newVertexStyle(id=2,shape="sphere", color="#00ff00"),
                'SUMULA':U.newVertexStyle(id=3,shape="sphere", color="#0000ff"),
                'REGIMENTO':U.newVertexStyle(id=4,shape="sphere", color="#0ff000"),
                }
    '''
    lei_style = U.newVertexStyle(id=1,shape="sphere", color="#ff0000")
    #Q = dbgrafo.execute(cf88_vs_outras_q)
    res = elist
    nodes = {}
    edges = set([])
    #print res[0]
    maxw = float(max(np.array([i[6] for i in res]))) #largest weight
    #U.beginMultiCall()
    c = 1
    for e in res:
        if e[0] not in nodes:
            n1 = U.newVertex(style=v_styles[e[1]], label=str(e[2]))
            nodes[e[0]] = n1
        else:
            n1 = nodes[e[0]]
        if e[3] not in nodes:
            n2 = U.newVertex(style=v_styles[e[4]], label=str(e[5]))
            nodes[e[3]] = n2
        else:
            n2 = nodes[e[3]]
        es = e[6]/maxw
        if (n1,n2) not in edges:
            U.newEdge(n1,n2,spline=True,strength=es, width=2.0, showstrain=True)
            edges.add((n1,n2))
            edges.add((n2,n1))
        c += 1
    #U.endMultiCall()
    

def cf88_vs_outras(nedges):
    """
    Desenha grafo via networkx
    para grafos pequenos.
    """
    G = nx.DiGraph()
    Q = dbgrafo.execute(cf88_vs_outras_q)
    res = Q.fetchmany(nedges)#[0]
    G.add_weighted_edges_from(res)
    nx.draw(G)
    #nx.draw_graphviz(G, "fdp")
    nx.write_dot(G, 'grafo_cf_vs_outras_%s.dot'%nedges)
    P.savefig('grafo_cf_vs_outras_%s.png'%nedges)
    return G

def lei_vs_lei(nedges=None):
    """
    Grafo de todas com todas (leis)
    """
    # Verão original Flávio comentada
    # Q = dbgrafo.execute('select lei_id_1,esfera_1,lei_1,lei_id_2,esfera_2, lei_2, peso from vw_gr_lei_lei where  peso >300 and lei_id_2>2')
    # Q = dbgrafo.execute('select lei_id_1,lei_tipo_1,lei_nome_1,lei_id_2,lei_tipo_2, lei_nome_2, peso from vw_gr_lei_lei where lei_count <= 20 and lei_id_1 = 1 and lei_id_2 <= 20 limit 0,1000')
    # Q = dbgrafo.execute('select lei_id_1,lei_tipo_1,lei_nome_1,lei_id_2,lei_tipo_2, lei_nome_2, peso from vw_gr_lei_lei where lei_count <= 8 and lei_id_1 <= 20 and lei_id_2 <= 20 limit 0,1000')
    curgrafo.execute('select lei_id_1,esfera_1,lei_1,lei_id_2,esfera_2, lei_2, peso from vw_gr_lei_lei where lei_count <= 10 and lei_id_1 <= 50 and lei_id_2 <= 200 limit 0,10000')
    if not nedges:
        res = curgrafo.fetchall()
        nedges = len(res)
    else:
        res = curgrafo.fetchmany(nedges)
    eds = [(i[0],i[3],i[6]) for i in res]
    G = nx.Graph()
    #eds = [i[:3] for i in res]
    G.add_weighted_edges_from(eds)
    print "== Grafo Lei_Lei =="
    print "==> Order: ",G.order()
    print "==> # Edges: ",len(G.edges())

    return G,res

def artigo_artigo(nedges=None):
    """
    grafo de artigos de leis
    """
    
    curgrafo.execute('select artigo_id_1,esfera_1,artigo_1,lei_1,artigo_id_2,esfera_2, artigo_2, lei_2, peso from vw_gr_artigo_artigo where  peso >100')
    if not nedges:
        res = curgrafo.fetchall()
        nedges = len(res)
    else:
        res = curgrafo.fetchmany(nedges)
    eds = [(i[0],i[4],i[8]) for i in res]
    G = nx.Graph()
    G.add_weighted_edges_from(eds)
    return G, eds

def ministro_lei(nedges=0):
    """
    Cria multigrafo de Ministros e leis
    """
    curgrafo.execute('select origid, destid, weight from gr_ministro_lei where weight >100')
    if not nedges:
        res = curgrafo.fetchall()
        nedges = len(res)
    else:
        res = curgrafo.fetchmany(nedges)
    eds = [(str(i[0]).decode('latin-1'),i[1],i[2]) for i in res]
    G = nx.DiGraph(nome='ministro_lei')
    G.add_weighted_edges_from(eds)
    return G, eds
    
def salva_grafoNX_imagem(G):
    """
    Salva grafos em formato png e dot
    """
    nx.draw_graphviz(G)
    nx.write_dot(G, 'relatorios/grafo_lei_vs_lei.dot')
    P.savefig('relatorios/grafo_lei_vs_lei.png')
    
@timeit
def cria_grafoNX_de_tabela (db, tabela):
    """
    Cria multigrafo a partir de uma tabela no banco.
    Cria apenas vertices. arestas serao adicionadas posteriormente
    """
    G = nx.MultiGraph(nome=tabela)
    Q =db.execute('select * from %s'%tabela)
    vnames  = Q.keys()
    for r in Q:
        attrs = dict(zip(vnames[1:], r[1:]))
        G.add_node(r[0], **attrs)
    return G

@timeit
def salva_grafoNX_db(G):
    """
    Salva pickle compactado do grafo como um blob no Banco
    """
    gp = gzip.zlib.compress(cPickle.dumps(G, protocol=2))
    dbdec.nx_grafo.insert(nome=G.graph['nome'], grafo=gp)
    dbdec.commit()

@timeit
def salva_grafoNX_file(G):
    """
    Salva pickle de grafo em disco 
    """
    gp = gzip.zlib.compress(cPickle.dumps(G, protocol=2))
    with open(G.graph['nome']+'.pickle.gz', 'wb') as f:
        f.write(gp)

@timeit
def le_grafoNX_file(nome):
    with open(nome+'.pickle.gz', 'rb') as f:
        gp = f.read()
    G = cPickle.loads(gzip.zlib.decompress(gp))
    return G

@timeit
def le_grafoNX_db(nome):
    g = dbdec.nx_grafo.filter(dbdec.nx_grafo.nome == nome).one()
    G = cPickle.loads(gzip.zlib.decompress(g.grafo))
    return G

def graph_stats(G):
    print "== Grafo Artigo_Artigo == "
    print "==> Order: ",G.order()
    print "==> # Edges: ",len(G.edges())
    print "==> # Cliques: ", nx.algorithms.clique.graph_number_of_cliques(G)
    try:
        print "==> Avg. Clustering: ", nx.average_clustering(G)
    except NetworkXError:
        pass
if __name__=="__main__":
#    dbgrafo = SqlSoup("%s/SEN_Grafo" % MySQLServer)
#    dbdec = SqlSoup("%s/STF_Analise_Decisao" % MySQLServer)
#    cf88_vs_outras(500)
#    dyn_graph(1000)
#    G,elist = lei_vs_lei()
#    nx.write_graphml(G,'lei_lei.graphml')
#    nx.readwrite.gpickle.write_gpickle(G, 'lei_lei.gpickle')
#    artigo_artigo()
    G,elist = ministro_lei()
    nx.write_graphml(G,'ministro_lei.graphml')
#    nx.readwrite.gpickle.write_gpickle(G, 'ministro_lei.gpickle')
#    G = cria_grafoNX_de_tabela(dbdec,'decisao')
#    salva_grafoNX_db(G)
#    G = le_grafoNX_db('decisao')
#    salva_grafoNX_file(G)
#    Gl = cria_grafoNX_de_tabela(dbdec,'lei_decisao')
#    salva_grafoNX_file(Gl)
#    G = le_grafoNX_file('decisao')
    graph_stats(G)
#    P.show()
    #~ dyn_graph_general(elist,G.order())
    
