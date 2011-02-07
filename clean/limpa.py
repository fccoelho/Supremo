import difflib
from collections import defaultdict
import re
#from sqlalchemy.ext.sqlsoup import SqlSoup
from BeautifulSoup import BeautifulSoup
#db = SqlSoup('mysql://root:password@emapserv/Supremo')
#print db.t_decisoes.all()
import MySQLdb

#Configura conexoes
db=MySQLdb.connect(host="emapserv", user="root", passwd="password",db="Supremo")
cur=db.cursor()

def busca_UF(texto):
    """
    localiza e extrai referencias a unidade federal 
    que originou o processo
    """
    rawstr = r"""(UF-(\D\D))+"""
    embedded_rawstr = r"""(UF-(\D\D))+"""
    compile_obj = re.compile(rawstr)
    match_obj = compile_obj.search(texto)
    if match_obj:
#        print match_obj.groups()
        return match_obj.groups()[1]
    
    
def conta_campos(cursor):
    cursor.execute('select decisao from t_decisoes limit 10000')
    decisoes = cursor.fetchmany(10000)
#    print decisoes
    campos = set([])
    for d in decisoes:
        s = BeautifulSoup(d[0].strip('[]'),  fromEncoding='IBM855')
#        print s.originalEncoding
        h = [i.contents[0] for i in s.findAll('strong') if  len(i.contents)==1 and len(i.contents[0]) <16]
#        print h
        cs = set(h)
#        print cs
#TODO: contar ocorrencias usando defaultdict
        campos.update(cs)
    return campos
    
def extrai_dados(cursor):
    """
    Constroi nova tabela com Datas, Estado e leis referenciadas
    """
    cursor.execute('select decisao,data_publicacao,data_decisao from t_decisoes limit 100,1000')
    dados = cursor.fetchmany(10)
    for d in dados:
        s = BeautifulSoup(d[0].strip('[]'),  fromEncoding='IBM855')
        c = s.findAll('pre')
        UFs = [busca_UF(t.contents[0]) for t in c]
        print UFs
#        print unicode(c),  type(c)
    
if __name__ == "__main__":
#    print conta_campos(cur)
    extrai_dados(cur)
