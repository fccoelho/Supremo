# -*- coding:utf-8 -*-
import re
import locale
from collections import defaultdict
from BeautifulSoup import BeautifulSoup
import MySQLdb
from MySQLdb.cursors import CursorUseResultMixIn,  DictCursor, SSDictCursor,  SSCursor

db=MySQLdb.connect(host="E04324", user="root", passwd="password",db="Supremo")
cur=db.cursor()

def analisa_votacao(cursor):
    """
    Analisa os resultados da votacao, buscando por
    ocorrencias dos lexemas derivados dos morfema
    'unam', como unanime, unanimidade, unanimamente;
    e o lexema 'maioria', que indica uma votacao não unanime
    """
    #expressoes a serem encontradas
    locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8') 
    rawstr1 = r"""(?u)UNÂN|UNAN|unan|unân"""
    rawstr2 = "MAIORIA"
    num_decisoes = 10000
    compile_obj1 = re.compile(rawstr1, re.LOCALE)
    compile_obj2 = re.compile(rawstr2, re.LOCALE)
    #buscando dados no banco
    cursor.execute('select decisao from Supremo.t_decisoes limit 10000')
    decisoes = cursor.fetchmany(num_decisoes)
    matches1 = 0
    matches2 = 0
    #extraindo expressoes dos dados recuperados
    for d in decisoes:
        sopa = BeautifulSoup(d[0].strip('[]'),  fromEncoding='ISO8859-1')
        texto = sopa.findAll('pre') 
        match_obj1 = compile_obj1.findall(str(texto))
        match_obj2 = compile_obj2.findall(str(texto))
        if match_obj1: matches1 +=1
        if match_obj2: matches2 +=1
        #print match_obj
    print 'Em', num_decisoes, 'decisoes, foram identificadas'
    print matches1, 'decisoes unanimes', '(', (100*matches1)/(matches1+matches2),'%) e' 
    print matches2, 'decisoes por maioria', '(', (100*matches2)/(matches1+matches2),'%).'
    cursor.close()

analisa_votacao(cur)
db.close()
