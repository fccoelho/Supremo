# -*- coding:utf-8 -*-
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
num_reg = 10
consulta_banco = 'select decisao from Supremo.t_decisoes limit %s,%s;'%(reg_inicio, num_reg)
match_string1 =  r"""unân[A-Z,a-z]{3,8}|unan[A-Z,a-z]{3,8}|UNÂN[A-Z,a-z]{3,8}|UNAN[A-Z,a-z]{3,8}|Unân[A-Z,a-z]{3,8}|Unan[A-Z,a-z]{3,8}"""
match_string2 = 'MAIORIA'

def busca_expressoes(cursor,  querydb, num_registros, rawstr1, rawstr2=''):
    """
    Recebe expressoes e uma consulta e busca por ocorrencias
    destas nos resultados da consulta
    """
    #locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8') 
    compile_obj1 = re.compile(rawstr1)#, re.LOCALE)
    compile_obj2 = re.compile(rawstr2)#, re.LOCALE)
    cursor.execute(querydb)
    registros = cursor.fetchmany(num_registros)
    matches1 = 0
    matches2 = 0
    dec_analise = []
    for d in registros:
        sopa = BeautifulSoup(d[0].strip('[]'),  fromEncoding='ISO8859-1')
        texto = sopa.findAll('pre') 
        match_obj1 = compile_obj1.findall(str(texto))
        if rawstr2: match_obj2 = compile_obj2.findall(str(texto))
        else: match_obj2 = ''
        if not match_obj1 and not match_obj2: dec_analise.append(texto)   
        if match_obj1: matches1 +=1
        if match_obj2: matches2 +=1
    print 'foram encontrados',  matches1, '(', ((matches1/num_registros)*100),'%)','da expressao',  match_obj1
    if rawstr2: print 'foram encontrados',  matches2, 'da expressao',  match_obj2
    return matches1, matches2
    cursor.close()

"""Main Code"""
busca_expressoes(cur, consulta_banco,  num_reg,  match_string1, match_string2)
db.close()
