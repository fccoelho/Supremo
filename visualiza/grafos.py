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

v_colors = {'LEG-FED':"#ff0000",
            'LEG-EST':"#00ff00",
            'LEG-MUN':"#0000ff"
            }


def dyn_graph_lei(elist):
    """
    Visualização dinâmica usando ubigraph
    Servidor Ubigraph deve estar rodando na URL indicada
    """
    if socket.gethostname()=='E04679':# Versão Flávio
        U = ubigraph.Ubigraph(URL='http://10.250.46.208:20738/RPC2')
    else:# Versão Pablo
        U = ubigraph.Ubigraph(URL='http://127.0.0.1:20738/RPC2')
    U.clear()
    v_styles = {'LEG-FED':U.newVertexStyle(id=1,shape="cube", color="#ff0000"),
                'LEG-EST':U.newVertexStyle(id=2,shape="cube", color="#00ff00"),
                'LEG-MUN':U.newVertexStyle(id=3,shape="cube", color="#0000ff"),
                'LEG-DIS':U.newVertexStyle(id=4,shape="cube", color="#0ff000"),
                'LEG-INT':U.newVertexStyle(id=5,shape="cube", color="#000ff0"),
                'outras':U.newVertexStyle(id=6,shape="cube", color="#f0f000"),
                }
    lei_style = U.newVertexStyle(id=1,shape="cube", color="#ff0000")
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
            U.newEdge(n1,n2,spline=True,strength=es, width=es)
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
    Q = dbgrafo.execute('select lei_id_1,esfera_1,lei_1,lei_id_2,esfera_2, lei_2, peso from vw_gr_lei_lei where  peso >300 and lei_id_2>2')
    if not nedges:
        res = Q.fetchall()
        nedges = len(res)
    else:
        res = Q.fetchmany(nedges)
    eds = [(i[0],i[3],i[6]) for i in res]
    G = nx.Graph()
    #eds = [i[:3] for i in res]
    G.add_weighted_edges_from(eds)
    print "== Grafo Lei_Lei =="
    print "==> Order: ",G.order()
    print "==> # Edges: ",len(G.edges())
    #nx.draw_random(G)
    #nx.draw_graphviz(G)
    #nx.write_dot(G, 'grafo_lei_vs_lei_%s.dot'%nedges)
    #P.savefig('grafo_lei_vs_lei_%s.png'%nedges)
    return G,res

def artigo_artigo(nedges=None):
    """grafo de artigos de leis"""
    
    Q = dbgrafo.execute('select artigo_id_1,esfera_1,artigo_1,lei_1,artigo_id_2,esfera_2, artigo_2, lei_2, peso from vw_gr_artigo_artigo where  peso >100')
    if not nedges:
        res = Q.fetchall()
        nedges = len(res)
    else:
        res = Q.fetchmany(nedges)
    eds = [(i[0],i[4],i[8]) for i in res]
    G = nx.Graph()
    G.add_weighted_edges_from(eds)
    print "== Grafo Artigo_Artigo == "
    print "==> Order: ",G.order()
    print "==> # Edges: ",len(G.edges())
    print "==> # Cliques: ", nx.algorithms.clique.graph_number_of_cliques(G)
    print "==> Avg. Clustering: ", nx.average_clustering(G)
        
if __name__=="__main__":
    import socket
    if socket.gethostname() == 'E04679':# versão Flávio
        dbgrafo = SqlSoup("mysql://root:password@E04324/SEN_Grafo")
        dbdec = SqlSoup("mysql://root:password@E04324/STF_Analise_Decisao")
    else:# versão Pablo
        dbgrafo = SqlSoup("mysql://pablo:pablo@E04324.fgv.br/SEN_Grafo")
        dbdec = SqlSoup("mysql://pablo:pablo@E04324.fgv.br/STF_Analise_Decisao")
    #cf88_vs_outras(500)
    #dyn_graph(1000)
    G,elist = lei_vs_lei()
    artigo_artigo()
    
    #P.show()
    dyn_graph_lei(elist)
    
