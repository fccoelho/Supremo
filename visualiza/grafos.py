# -*- coding:utf-8 -*-
'''
Created on 05/04/2011

@author: flavio
'''
import networkx as nx
import xmlrpclib
import os, time
from sqlalchemy.ext.sqlsoup import SqlSoup
import numpy as np
import matplotlib.pyplot as P
from matplotlib.colors import rgb2hex
from matplotlib import cm
import ubigraph

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


def dyn_graph(elist):
    """
    Visualização dinâmica usando ubigraph
    Servidor Ubigraph deve estar rodando na URL indicada
    """
    # Versão Flávio
    # U = ubigraph.Ubigraph(URL='http://10.250.46.208:20738/RPC2')
    # Versão Pablo
    U = ubigraph.Ubigraph(URL='http://127.0.0.1:20738/RPC2')
    U.clear()
    #cf_style = U.newVertex(id=0,shape="cube", color="#ffff00")
    lei_style = U.newVertexStyle(id=1,shape="cube", color="#ff0000")
    #Q = dbgrafo.execute(cf88_vs_outras_q)
    res = np.array(elist)
    nodes = {}
    edges = set([])
    #print res[0]
    maxw = float(max(res[:,2])) #largest weight
    #U.beginMultiCall()
    c = 1
    for e in res:
        #print "%s\r"%c,
        #if not c%100:
        #    time.sleep(.5)
        #print e, e[0],e[1],e[2]
        if e[0] not in nodes:
            n1 = U.newVertex(style=lei_style, label=str(e[0]))
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
            U.newEdge(n1,n2,spline=False,strength=es, width=es)
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
    Grafo de todas com todas
    """
    Q = dbgrafo.execute('select lei_id_1,lei_id_2, peso from gr_lei_lei where peso >400 and lei_id_1 >2 and lei_id_2>2')
    if not nedges:
        res = Q.fetchall()
        nedges = len(res)
    else:
        res = Q.fetchmany(nedges)
    G = nx.DiGraph()
    #eds = [i[:3] for i in res]
    G.add_weighted_edges_from(res)
    #nx.draw_random(G)
    #nx.draw_graphviz(G)
    #nx.write_dot(G, 'grafo_lei_vs_lei_%s.dot'%nedges)
    #P.savefig('grafo_lei_vs_lei_%s.png'%nedges)
    return G,res
    
if __name__=="__main__":
    # versão Flávio
    # dbgrafo = SqlSoup("mysql://root:password@E04324/SEN_Grafo")
    # dbdec = SqlSoup("mysql://root:password@E04324/STF_Analise_Decisao")
    # versão Pablo
    dbgrafo = SqlSoup("mysql://pablo:pablo@E04324.fgv.br/SEN_Grafo")
    dbdec = SqlSoup("mysql://pablo:pablo@E04324.fgv.br/STF_Analise_Decisao")
    #cf88_vs_outras(500)
    #dyn_graph(1000)
    G,elist = lei_vs_lei()
    print G.order()
    print len(G.edges())
    #P.show()
    dyn_graph(elist)
    
