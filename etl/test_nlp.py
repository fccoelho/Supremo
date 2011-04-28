# -*- coding:utf-8 -*-
"""
testes para modulo nlp
"""
from nlp  import *

def test_find_re():
    texto = ['Un\xc3\xa2nime,', 'UN\xc3\x82NIME,', 'un\xc3\xa2nime', 'un\xc3\xa2nime,', 'unanimidade', 'Un\xc3\xa2nime', 'unanimemente', 'UN\xc3\x82NIMEMENTE', 'UNANIMIDADE', 'unanimimente', 'Unanimemente', 'unanimidade,', 'un\xc3\xa2nie,', 'UN\xc3\x82NIME', 'un\xc3\xa2nimes,', 'unanimenete', 'UNANIMIDADE,']
    rex = r"""unân[A-Z,a-z]{3,8}|unan[A-Z,a-z]{3,8}|UNÂN[A-Z,a-z]{3,8}|UNAN[A-Z,a-z]{3,8}|Unân[A-Z,a-z]{3,8}|Unan[A-Z,a-z]{3,8}"""
    crex = re.compile(rex)
    assert len(find_re(texto, crex)) == len(texto)
    
def test_unicode_find_re():
    cur.execute(consulta_banco)
    decisao = cur.fetchone()
    sopa1 = BeautifulSoup(decisao[0].strip('[]'),  fromEncoding='ISO8859-1')
    ementa = sopa1.findAll('pre') 
    rex = r"""unân[A-Z,a-z]{3,8}|unan[A-Z,a-z]{3,8}|UNÂN[A-Z,a-z]{3,8}|UNAN[A-Z,a-z]{3,8}|Unân[A-Z,a-z]{3,8}|Unan[A-Z,a-z]{3,8}"""
    crex = re.compile(rex)
    assert len(find_re(ementa, crex)) > 0

def test_lowercase_find_re():
    cur.execute(consulta_banco)
    decisao = cur.fetchone()
    sopa1 = BeautifulSoup(decisao[0].strip('[]'),  fromEncoding='ISO8859-1')
    ementa = sopa1.findAll('pre') 
    ementa  = [str(s).lower() for s in ementa if s]
    print ementa
    rex = r"""unân[A-Z,a-z]{3,8}|unan[A-Z,a-z]{3,8}"""
    crex = re.compile(rex.decode('ISO8859-1'))
    assert len(find_re(ementa, crex)) > 0
