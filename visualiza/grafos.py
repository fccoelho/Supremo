# -*- coding:utf-8 -*-
'''
Created on 05/04/2011

@author: flavio
'''
import networkx as nx
import xmlrpclib
import os
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

def dyn_graph(nedges):
    """
    Visualização dinâmica usando ubigraph
    Servidor Ubigraph deve estar rodando
    """
    U = ubigraph.Ubigraph(URL='e04324:20738/RPC2')
    U.clear()
    cf_style = U.newVertex(id=0,shape="sphere", color="#ffff00")
    lei_style = U.newVertexStyle(id=1,shape="sphere", color="#ff0000")
    Q = dbgrafo.execute(cf88_vs_outras_q)
    res = np.array(Q.fetchmany(nedges))
    nodes = {}
    for e in res:
        #print e, e[0],e[1],e[2]
        if e[0] not in nodes:
            n1 = U.newVertex(style=cf_style, label=str(e[0]))
            nodes[e[0]] = n1
        else:
            n1 = nodes[e[0]]
        if e[1] not in nodes:
            n2 = U.newVertex(style=lei_style, label=str(e[1]))
            nodes[e[1]] = n2
        else:
            n2 = nodes[e[1]]
        es = e[2]/max(res[:,2])
        U.newEdge(n1,n2,spline=False,strength=es, width=str(es))

def cf88_vs_outras(nedges):
    G = nx.DiGraph()
    Q = dbgrafo.execute(cf88_vs_outras_q)
    res = Q.fetchmany(nedges)#[0]
    G.add_weighted_edges_from(res)
    nx.draw(G)
    nx.draw_graphviz(G, "fdp")
    nx.write_dot(G, 'grafo_cf_vs_outras_%s.dot'%nedges)
    P.savefig('grafo_cf_vs_outras_%s.png'%nedges)


if __name__=="__main__":
    dbgrafo = SqlSoup("mysql://root:password@E04324/SEN_Grafo")
    dbdec = SqlSoup("mysql://root:password@E04324/STF_Analise_Decisao")
    #cf88_vs_outras(500)
    dyn_graph(1000)
    P.show()