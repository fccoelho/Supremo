# -*- coding:utf-8 -*-
from __future__ import division
import re
import locale
from collections import defaultdict
from BeautifulSoup import BeautifulSoup
import MySQLdb
from MySQLdb.cursors import CursorUseResultMixIn,  DictCursor, SSDictCursor,  SSCursor
import numpy as np
import matplotlib.pyplot as plt
import pylab
from matplotlib.patches import Polygon
from matplotlib.ticker import MaxNLocator

"""Variaveis Globais"""
db=MySQLdb.connect(host="E04324.fgv.br", user="root", passwd="password",db="Supremo")
cur=db.cursor()
reg_inicio = 0
num_reg = 100
consulta_banco = 'select decisao, tipo from Supremo.t_decisoes limit %s,%s;'%(reg_inicio, num_reg)
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
    
def busca_expressoes(cursor,  querydb, num_registros, expressao1,  expressao2=''):
    """
    Recebe 1 ou 2 expressao(oes). Compila com a funcao <find_re>. Recebe um cursor de conexao ao banco.
    Recebe uma query para este banco e executa a query limitada pelo numero de registros recebido
    Busca por ocorrencias desta(s) expressao(oes) compilada nos resultados.
    Devolve # registros que satisfazem e # registros que não satisfazem
    Devolve conjunto dos matches compilados encontrados em todos os registros para cada expressao
    Devolve, para cada expressao listas de tuplas, associando os registros aos tipos de decisao.
    """
    num_nomatches = 0
    lista_nomatches = []
    conj_decisao_tipo = set()
    dic_matches1_tipo = {}
    num_matches1 = 0
    lista_matches1 = []
    conj_matches1 = set()
    compile_obj1 = re.compile(expressao1)
    if expressao2:                                             # So executa bloco se forem passadas duas expressoes
        dic_matches2_tipo = {}
        num_matches2 = 0
        lista_matches2 = []
        conj_matches2 = set()
        compile_obj2 = re.compile(expressao2)
    cursor.execute(querydb)
    registros_db = cursor.fetchmany(num_registros)
    for registro in registros_db:                       #registro eh uma tupla (decisao,tipo), de acordo com as tabelas do banco
        decisao_texto = BeautifulSoup(registro[0].strip('[]'),  fromEncoding='ISO8859-1')
        ementa = decisao_texto.findAll('pre')   # A ementa esta envolta em uma marcacao HTML <pre> no texto da decisao
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
    cursor.close()
    for match, tipo in lista_matches1: dic_matches1_tipo[tipo] = (dic_matches1_tipo.get(tipo, 0) +1)
    if num_matches2:
        for match, tipo in lista_matches2: dic_matches2_tipo[tipo] = (dic_matches2_tipo.get(tipo, 0) +1)
        return lista_nomatches,  num_nomatches,\
                    dic_matches1_tipo, num_matches1, conj_matches1, lista_matches1,\
                    dic_matches2_tipo, num_matches2, conj_matches2, lista_matches2
    else:
        return lista_nomatches,  num_nomatches,\
                    dic_matches1_tipo, num_matches1,  conj_matches1, lista_matches1


def desenha_grafico (dict1,  dict2={})
    val = dict1.    # the bar lengths
    pos = arange(5)+.5    # the bar centers on the y axis
    figure(1)
    barh(pos,val, align='center')
    yticks(pos, ('Tom', 'Dick', 'Harry', 'Slim', 'Jim'))
    xlabel('Performance')
    title('Resultados por tipo de decisao')
    grid(True)
    show()

"""Main Code"""
if __name__=="__main__":
    resultado = busca_expressoes(cur, consulta_banco,  num_reg,  match_string1,  match_string2)
    db.close()
    print 'A(s) expressao(oes)',  list(resultado[4])
    print 'ocorrem em', resultado[3], 'dos', num_reg, 'registros analisados'
    print '(', ((resultado[3]/num_reg)*100),'%)'
    print resultado[2]   
    if len(resultado) >= 9:
        print 'A(s) expressao(oes)',  list(resultado[8])
        print 'ocorrem em', resultado[7],'dos', num_reg, 'registros analisados'
        print'(', ((resultado[7]/num_reg)*100),'%)'
        print resultado[6]
    #desenha_grafico(resultado[2], resultado[6])
"""End"""
