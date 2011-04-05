'''
Created on 05/04/2011

@author: flavio
'''
import networkx as nx
from sqlalchemy.ext.sqlsoup import SqlSoup
import numpy as np
import matplotlib.pyplot as P

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

def cf88_vs_outras(nedges):
    G = nx.DiGraph()
    Q = dbgrafo.execute(cf88_vs_outras_q)
    res = Q.fetchmany(nedges)#[0]
    G.add_weighted_edges_from(res)
    nx.draw(G)


if __name__=="__main__":
    dbgrafo = SqlSoup("mysql://root:password@E04324/SEN_Grafo")
    dbdec = SqlSoup("mysql://root:password@E04324/STF_Analise_Decisao")
    cf88_vs_outras(500)
    P.show()