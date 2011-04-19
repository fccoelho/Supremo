# -*- coding:utf-8 -*-
import re
import locale
from collections import defaultdict
from BeautifulSoup import BeautifulSoup
import MySQLdb
from MySQLdb.cursors import CursorUseResultMixIn,  DictCursor, SSDictCursor,  SSCursor

db=MySQLdb.connect(host="E04324", user="root", passwd="password",db="Supremo")
cur=db.cursor()
reg_inicio = 0
num_reg = 100
consulta_banco = 'select decisao from Supremo.t_decisoes limit %s,%s;'%(reg_inicio, num_reg)
match_string1 = r"""(?u)UNÂN|UNAN|unan|unân"""
match_string2 = "MAIORIA"

def busca_expressao(cursor,  querydb, rawstr,  num_registros):
    """
    Recebe uma expressao e uma consulta e busca por ocorrencias
    da expressao nos resultados da consulta
    """
    locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8') 
    compile_obj = re.compile(rawstr, re.LOCALE)
    cursor.execute(querydb)
    registros = cursor.fetchmany(num_registros)
    matches = 0
    # extraindo expressoes dos dados recuperados
    for d in registros:
        sopa = BeautifulSoup(d[0].strip('[]'))#,  fromEncoding='ISO8859-1')
        texto = sopa.findAll('pre') 
        match_obj = compile_obj.findall(str(texto))
        if match_obj: matches +=1
    #print matches,  match_obj
    return matches,  match_obj
    cursor.close()

def busca_expressoes(cursor,  querydb, rawstr1,  rawstr2,  num_registros):
    """
    Recebe expressoes e uma consulta e busca por ocorrencias
    destas nos resultados da consulta
    """
    locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8') 
    compile_obj1 = re.compile(rawstr1, re.LOCALE)
    compile_obj2 = re.compile(rawstr2, re.LOCALE)
    cursor.execute(querydb)
    registros = cursor.fetchmany(num_registros)
    matches1 = 0
    matches2 = 0
    # extraindo expressoes dos dados recuperados
    for d in registros:
        sopa = BeautifulSoup(d[0].strip('[]'))#,  fromEncoding='ISO8859-1')
        texto = sopa.findAll('pre') 
        match_obj1 = compile_obj1.findall(str(texto))
        match_obj2 = compile_obj2.findall(str(texto))
        if not match_obj1 and not match_obj2: print texto   
        if match_obj1: matches1 +=1
        if match_obj2: matches2 +=1
    print matches1,  match_obj1
    print matches2,  match_obj2
    #return matches,  match_obj
    cursor.close()

#numero,  expressao = busca_expressao(cur, consulta_banco, match_string2, num_reg)
#print numero,  expressao

busca_expressoes(cur, consulta_banco,  match_string1, match_string2,  num_reg)

db.close()
