# -*- coding:utf-8 -*-
"""
Testes do módulo grafos.

"""
from grafos import *
import os

global dbgrafo, dbdec

def setup_func():
    "set up test fixtures"
    global dbgrafo, dbdec
    dbgrafo = SqlSoup("%s/SEN_Grafo" % MySQLServer)
    dbdec = SqlSoup("%s/STF_Analise_Decisao" % MySQLServer)
    
def teardown_func():
    "tear down test fixtures"
    os.unlink('teste.pickle.gz')
    
def test_salva_grafoNX_file():
    G = nx.MultiGraph(nome='teste')
    salva_grafoNX_file(G)
    assert os.path.exists(G.graph['nome']+'.pickle.gz')
    
def test_le_grafoNX_file():
    G = le_grafoNX_file('teste')
    assert isinstance(G,  nx.MultiGraph)
test_le_grafoNX_file.teardown = teardown_func
