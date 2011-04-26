# -*- coding:utf-8 -*-
from __future__ import division
import re
import locale
from collections import defaultdict
from BeautifulSoup import BeautifulSoup
import MySQLdb
from MySQLdb.cursors import CursorUseResultMixIn,  DictCursor, SSDictCursor,  SSCursor

"""Variaveis Globais"""
db=MySQLdb.connect(host="E04324", user="root", passwd="password",db="Supremo")
cur=db.cursor()
reg_inicio = 0
num_reg = 100
consulta_banco = 'select decisao, tipo from Supremo.t_decisoes limit %s,%s;'%(reg_inicio, num_reg)
match_string1 = r"""unân[A-Z,a-z]{3,8}|unan[A-Z,a-z]{3,8}|UNÂN[A-Z,a-z]{3,8}|UNAN[A-Z,a-z]{3,8}|Unân[A-Z,a-z]{3,8}|Unan[A-Z,a-z]{3,8}"""
match_string2 = r"""MAIORIA|Maioria|maioria"""

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
    

def busca_expressao1(cursor,  querydb, num_registros, expressao):
    """
    Recebe uma expressao. Compila com a funcao <find_re>. Recebe um cursor de conexao ao banco.
    Recebe uma query para este banco e executa a query limitada pelo numero de registros recebido
    Busca por ocorrencias desta expressao compilada nos resultados.
    Devolve # registros que satisfazem e # registros que não satisfazem
    Devolve conjunto dos matches compilados encontrados em todos os registros
    Devolve 2 listas de tuplas, associando os registros aos tipos de decisao.
    """
    num_matches = 0
    num_nomatches = 0
    lista_matches = []
    lista_nomatch = []
    conj_matches = set()
    #locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8') 
    compile_obj = re.compile(expressao)#, re.LOCALE)
    cursor.execute(querydb)
    decisoes = cursor.fetchmany(num_registros)
    for decisao in decisoes:                #decisao eh uma tupla (decisao,tipo)
        sopa1 = BeautifulSoup(decisao[0].strip('[]'),  fromEncoding='ISO8859-1')
        sopa2 = BeautifulSoup(decisao[1],  fromEncoding='ISO8859-1')
        ementa = sopa1.findAll('pre')  # A ementa da decisao esta em uma marcacao HTML <pre>
        match_obj = find_re(ementa, compile_obj) 
        if match_obj:                             # testa se achou a string recebida no texto
            lista_matches.append((str(match_obj[0]), str(sopa2)))
            for match in match_obj: conj_matches.add(str(match))
            num_matches +=1
        else:
            lista_nomatch.append((str(ementa), str(sopa2)))
            num_nomatches +=1
    cursor.close()
    return num_matches,  conj_matches,  lista_matches,  lista_nomatch,  num_nomatches
    

def busca_expressao2(tupla_resultado1, expressao):
    """
    Recebe uma expressao e a lista de tuplas <lista_nomatch> da funcao <busca_expressao>.
    Busca por ocorrencias desta expressao compilada nos resultados.
    Devolve # registros que satisfazem e # registros que não satisfazem
    Devolve conjunto dos matches compilados encontrados em todos os registros
    Devolve 2 listas de tuplas, associando os registros aos tipos de decisao.
    """
    num_matches = 0
    num_nomatches = 0
    lista_matches = []
    lista_nomatch = []
    conj_matches = set()
    #locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8') 
    compile_obj = re.compile(expressao)#, re.LOCALE)
    for tupla in tupla_resultado1:
        for texto in tupla[0]:
            match_obj = find_re(texto, compile_obj) 
            if match_obj:                             # testa se achou a string recebida no texto
                lista_matches.append((str(match_obj[0]), str(tupla[1])))
                for match in match_obj: conj_matches.add(str(match))
                num_matches +=1
            else:
                lista_nomatch.append((str(texto), str(tupla[1])))
                num_nomatches +=1
    return num_matches,  conj_matches,  lista_matches,  lista_nomatch,  num_nomatches


if __name__=="__main__":
    resultado1 = busca_expressao1(cur, consulta_banco,  num_reg,  match_string1)
    db.close()
    print 'A(s) expressao(oes)',  list(resultado1[1]), 'ocorrem em', resultado1[0]
    print 'dos', resultado1[0] + resultado1[4], 'registros analisados (', ((resultado1[0])/((resultado1[0] + resultado1[4]))*100),'%)'
    lista_nomatches = resultado1[3]
    resultado2 = busca_expressao2(lista_nomatches, match_string2)
    print 'A(s) expressao(oes)',  list(resultado2[1]), 'ocorrem em', resultado2[0]
    print 'dos', resultado2[0] + resultado2[4], 'registros analisados (', ((resultado1[0])/((resultado2[0] + resultado2[4]))*100),'%)'
"""End"""
