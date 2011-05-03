# -*- coding:utf-8 -*-
from __future__ import division
import re
import locale
from collections import defaultdict
from BeautifulSoup import BeautifulSoup
import MySQLdb
from MySQLdb.cursors import CursorUseResultMixIn,  DictCursor, SSDictCursor,  SSCursor
from pylab import *
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter
from matplotlib.patches import Polygon
from matplotlib.ticker import MaxNLocator

"""Variaveis Globais"""
db = MySQLdb.connect(host="E04324.fgv.br", user="root", passwd="password",db="Supremo_new")
match_string1 = r"""unân[A-Z,a-z]{3,8}|unan[A-Z,a-z]{3,8}|UNÂN[A-Z,a-z]{3,8}|UNAN[A-Z,a-z]{3,8}|Unân[A-Z,a-z]{3,8}|Unan[A-Z,a-z]{3,8}"""
match_string2 = r"""(?i)MAIORIA"""
#match_string3 = "Homologada", "erro material" (testar estas strings)

def find_re(texto, crex):
    """
    Retorna lista matches de expressao regular compilada "crex" em texto
    """
    matches = []
    #assert isinstance(texto, list)
    for t in texto:
        if not t:
            continue
        matches.extend(crex.findall(str(t)))
    return matches
    
def busca_expressoes(dbase, expressao1, expressao2=''):
    """
    Recebe uma conexao ao banco. Determina numero de registros da tabela
    Recebe 1 ou 2 expressao(oes). Compila com a funcao <find_re>.
    Busca por ocorrencias desta(s) expressao(oes) compilada nos resultados.
    Devolve # registros que satisfazem e # registros que não satisfazem
    Devolve conjunto dos matches compilados encontrados em todos os registros para cada expressao
    Devolve, para cada expressao listas de tuplas, associando os registros aos tipos de decisao.
    Devolve tambem dicionarios contendo {tipos de decisao: numero de matches para o tipo}
    """
    num_nomatches = 0
    lista_nomatches = []
    conj_decisao_tipo = set()
    dic_matches1_tipo = {}
    num_matches1 = 0
    lista_matches1 = []
    conj_matches1 = set()
    compile_obj1 = re.compile(expressao1)
    # So executa bloco se forem passadas duas expressoes
    if expressao2:
        dic_matches2_tipo = {}
        num_matches2 = 0
        lista_matches2 = []
        conj_matches2 = set()
        compile_obj2 = re.compile(expressao2)
    dbcursor=dbase.cursor()
    dbcursor.execute('select count(*) from Supremo_new.t_decisoes') #determina num registros na tabela
    num_reg = dbcursor.fetchone()[0]  
    dbcursor.close()
    reg_inicio = 0
    dbcursor=dbase.cursor()
    while reg_inicio < num_reg:                               # estrategia para nao estourar a memoria, processando 1000 de cada vez
        dbcursor.execute('select decisao, tipo from Supremo_new.t_decisoes limit %s,%s;'%(reg_inicio, 1000))
        registros_db=dbcursor.fetchmany(1)
        while registros_db != ():
            for registro in registros_db:                       #registro eh uma tupla (decisao,tipo), de acordo com as tabelas do banco
                decisao_texto = BeautifulSoup(registro[0].strip('[]'),  fromEncoding='ISO8859-1')
                ementa = decisao_texto.findAll('pre')   # a ementa esta envolta em uma marcacao HTML <pre> no texto da decisao
                match_obj1 = find_re(ementa, compile_obj1)
                decisao_tipo = registro[1]
                conj_decisao_tipo.add(decisao_tipo)
                if match_obj1:                                      # testa se achou a primeira expressao recebida no texto
                    lista_matches1.append((match_obj1, decisao_tipo))
                    for match in match_obj1: conj_matches1.add(match)
                    num_matches1 +=1
                elif expressao2:                                    # So executa bloco se forem passadas duas expressoes
                    match_obj2 = find_re(ementa, compile_obj2)
                    if match_obj2:                                  # testa se achou a segunda expressao recebida no texto
                        lista_matches2.append((match_obj2, decisao_tipo))
                        for match in match_obj2: conj_matches2.add(match)
                        num_matches2 +=1
                else:                                                   # se nao achou nenhuma das expressoes
                    lista_nomatches.append((ementa, decisao_tipo))
                    num_nomatches +=1
                registros_db=dbcursor.fetchmany(1)
        reg_inicio +=1000
        print 'Processando', reg_inicio, 'de', num_reg, 'registros' #para checar o andamento do processo
        print '(', ((reg_inicio/num_reg)*100),'%)'
    dbcursor.close()
    for match, tipo in lista_matches1: dic_matches1_tipo[tipo] = (dic_matches1_tipo.get(tipo, 0) +1)
    if num_matches2:
        for match, tipo in lista_matches2: dic_matches2_tipo[tipo] = (dic_matches2_tipo.get(tipo, 0) +1)
        return num_reg, lista_nomatches,  num_nomatches,\
                    dic_matches1_tipo, num_matches1, conj_matches1, lista_matches1,\
                    dic_matches2_tipo, num_matches2, conj_matches2, lista_matches2
    else:
        return num_reg, lista_nomatches,  num_nomatches,\
                    dic_matches1_tipo, num_matches1,  conj_matches1, lista_matches1


def desenha_grafico (dict):
    """
    http://matplotlib.sourceforge.net/examples/pylab_examples/barh_demo.html
    """
    val = dict.values()   # the bar lengths
    pos = arange(len(dict))+.5    # the bar centers on the y axis
    figure()
    yticks(pos, (dict.keys()))
    barh(pos,val, align='center')
    xlabel('Decisoes')
    title('Unanimidade por tipo de decisao')
    grid(True)
    
"""Main Code"""
if __name__=="__main__":
    resultado = busca_expressoes(db, match_string1,  match_string2)
    db.close()
    print 'A(s) expressao(oes)',  list(resultado[5])
    print 'ocorrem em', resultado[4], 'dos', resultado[0], 'registros analisados'
    print '(', ((resultado[4]/resultado[0])*100),'%)'
    print resultado[3]   
    desenha_grafico(resultado[3])
    if len(resultado) >= 10:
        print 'A(s) expressao(oes)',  list(resultado[9])
        print 'ocorrem em', resultado[8],'dos', resultado[0], 'registros analisados'
        print'(', ((resultado[8]/resultado[0])*100),'%)'
        print resultado[7]
        desenha_grafico(resultado[7])
    show()
"""End"""
