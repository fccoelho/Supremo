# -*- coding:utf-8 -*-
from __future__ import division
import re
import locale
from collections import defaultdict
from BeautifulSoup import BeautifulSoup
import MySQLdb
from MySQLdb.cursors import CursorUseResultMixIn,  DictCursor, SSDictCursor,  SSCursor

"""Variaveis Globais"""
db=MySQLdb.connect(host="E04324@fgv.br", user="root", passwd="password",db="Supremo")
cur=db.cursor()
reg_inicio = 0
num_reg = 10
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
    num_matches1 = 0
    num_nomatches1 = 0
    lista_matches1 = []
    lista_nomatch1 = []
    conj_matches1 = set()
    compile_obj1 = re.compile(expressao1)
    if expressao2:                                             # So executa bloco se forem passadas duas expressoes
        num_matches2 = 0
        num_nomatches2 = 0
        lista_matches2 = []
        lista_nomatch2 = []
        conj_matches2 = set()
        compile_obj2 = re.compile(expressao2)
    cursor.execute(querydb)
    registros_db = cursor.fetchmany(num_registros)
    for registro in registros_db:                       #registro eh uma tupla (decisao,tipo), de acordo com as tabelas do banco
        decisao_texto = BeautifulSoup(registro[0].strip('[]'),  fromEncoding='ISO8859-1')
        decisao_tipo = BeautifulSoup(registro[1],  fromEncoding='ISO8859-1')
        ementa = decisao_texto.findAll('pre')   # A ementa esta envolta em uma marcacao HTML <pre> no texto da decisao
        match_obj1 = find_re(ementa, compile_obj1)
        if match_obj1:                                      # testa se achou a primeira expressao recebida no texto
            lista_matches1.append((str(match_obj1[0]), str(decisao_tipo)))
            for match in match_obj1: conj_matches1.add(str(match))
            num_matches1 +=1
        elif expressao2:                                    # So executa bloco se forem passadas duas expressoes
            match_obj2 = find_re(ementa, compile_obj2)
            if match_obj2:                                  # testa se achou a segunda expressao recebida no texto
                lista_matches2.append((str(match_obj2[0]), str(decisao_tipo)))
                for match in match_obj2: conj_matches2.add(str(match))
                num_matches2 +=1
        else:                                                   # se nao achou nenhuma das expressoes
            lista_nomatch.append((ementa, str(decisao_tipo)))
            num_nomatches +=1
    cursor.close()
    if expressao2:
        return lista_nomatch,  num_nomatches,  num_matches1,  conj_matches1,  lista_matches1, num_matches2,  conj_matches2,  lista_matches2
    else:
        return lista_nomatch,  num_nomatches,  num_matches1,  conj_matches1,  lista_matches1
        
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
            lista_nomatch.append((ementa, str(sopa2)))
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
        match_obj = find_re(tupla[0], compile_obj)
        if match_obj:                             # testa se achou a string recebida no texto
            lista_matches.append((str(match_obj[0]), str(tupla[1])))
            for match in match_obj: conj_matches.add(str(match))
            num_matches +=1
        else:
            lista_nomatch.append((tupla[0], str(tupla[1])))
            num_nomatches +=1
    return num_matches,  conj_matches,  lista_matches,  lista_nomatch,  num_nomatches

"""Main Code"""
if __name__=="__main__":
    resultado1 = busca_expressao1(cur, consulta_banco,  num_reg,  match_string1)
    db.close()
    print 'A(s) expressao(oes)',  list(resultado1[1])
    print 'ocorrem em', resultado1[0], 'dos', resultado1[0] + resultado1[4], 'registros analisados'
    print '(', ((resultado1[0])/((resultado1[0] + resultado1[4]))*100),'%)'
    print
    print 'Passamos a processar os',  resultado1[4], 'registros em que a primeira expressao nao foi encontrada...'
    lista_nomatches = resultado1[3]
    resultado2 = busca_expressao2(lista_nomatches, match_string2)
    print 'A(s) expressao(oes)',  list(resultado2[1])
    print 'ocorrem em', resultado2[0],'dos', resultado2[0] + resultado2[4], 'registros analisados'
    print'(', ((resultado2[0])/((resultado2[0] + resultado2[4]))*100),'%)'
    print 'ou seja, em', ((resultado2[0])/((resultado1[0] + resultado1[4]))*100),'% dos', resultado1[0] + resultado1[4], 'registros totais analisados'
    #print resultado2[3]
"""End"""
