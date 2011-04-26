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
num_reg = 10000
consulta_banco = 'select decisao, tipo from Supremo.t_decisoes limit %s,%s;'%(reg_inicio, num_reg) #TODO acrescentar campo tipo da decisao na query
match_string1 =  r"""unân[A-Z,a-z]{3,8}|unan[A-Z,a-z]{3,8}|UNÂN[A-Z,a-z]{3,8}|UNAN[A-Z,a-z]{3,8}|Unân[A-Z,a-z]{3,8}|Unan[A-Z,a-z]{3,8}"""
match_string2 = 'MAIORIA'

def busca_expressao(cursor,  querydb, num_registros, rawstr):
    """
    Recebe uma expressao e uma consulta e busca
    por ocorrencias desta nos resultados da consulta
    """
    num_matches = 0
    lista_matches = []
    lista_nomatch = []
    conj_matches = set()
    #locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8') 
    compile_obj = re.compile(rawstr)#, re.LOCALE)
    cursor.execute(querydb)
    decisoes = cursor.fetchmany(num_registros)
    for decisao in decisoes:                #decisao eh uma tupla (decisao,tipo)
        sopa1 = BeautifulSoup(decisao[0].strip('[]'),  fromEncoding='ISO8859-1')
        sopa2 = BeautifulSoup(decisao[1],  fromEncoding='ISO8859-1')
        ementa = sopa1.findAll('pre')  # A ementa da decisao esta em uma marcacao HTML <pre>
        match_obj = compile_obj.findall(str(ementa))
        if match_obj:                             # testa se achou a string recebida no texto
            lista_matches.append((str(match_obj[0]), str(sopa2)))
            for match in match_obj: conj_matches.add(str(match))
            num_matches +=1
        else: lista_nomatch.append((str(ementa), str(sopa2)))
    cursor.close()
    return num_matches,  conj_matches,  lista_matches,  lista_nomatch
    

def analisa_resultado(resultado,  rawstr):
    """
    Analisa os resultados 
    """

"""Main Code"""
resultado = busca_expressao(cur, consulta_banco,  num_reg,  match_string1)
db.close()
print 'A(s) expressao(oes)',  list(resultado[1]), 'ocorrem em', resultado[0]
print 'dos', num_reg, 'registros analisados (', ((resultado[0])/((num_reg))*100),'%)'
#analisa_resultado(resultado, match_string2)
"""End"""
