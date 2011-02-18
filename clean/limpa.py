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
    rawstr =r"\s/\s([A-Z]{2})\s+-"
    compile_obj = re.compile(rawstr)
    match_obj = compile_obj.search(texto)
#    print texto
    if match_obj:
#        print match_obj.groups()
        return match_obj.groups()[0]
        
class BuscaLeis:
    def __init__(self, texto):
        self.leisfed = []
        self.leisest = []
        self.leismun = []
        self.split_leis(texto)
    def split_leis(self, texto):
        """
        
        
    
def busca_leis(texto):
    """
    Localiza e extrai referencias a Leis na decisao judicail
    """
    rawstr = r""">*\s*([A-Z]{2,3}-[A-Z,0-9]*)|(CF)|("CAPUT")\s+"""
    compile_obj = re.compile(rawstr)
    match_obj = compile_obj.findall(texto)
    matches = []
    for m in match_obj:
        matches.append([i for i in m if i][0])
    print "texto: ", texto
    print "matches: ", matches

    
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
    
def extrai_dados(cursor,  inicio,  num):
    """
    Constroi nova tabela com Datas, Estado e leis referenciadas
    cursor ...
    """
    cursor.execute('select decisao,tipo,data_publicacao,data_decisao from t_decisoes limit %s,%s'%(inicio, num))
    dados = cursor.fetchmany(num)
    UFs = []
    for d in dados:
        sopa = BeautifulSoup(d[0].strip('[]'),  fromEncoding='IBM855')
#        print sopa.originalEncoding
        # Tag contendo informacao de UF
        c = sopa.strong
        uf = busca_UF(c.contents[0])
#        print uf
        if uf:
            UFs.append(uf)
        else:
            UFs.append('NA')

        # Tag contendo legislacao
        rs  = sopa.findAll('strong', text=re.compile('^Legisla'))
        if rs:
            l = rs[0].next.nextSibling
            legs = busca_leis(l.contents[0])
    print "Falhas em Extracao de UFs: ",  num-len(UFs)
#        print unicode(c),  type(c)
    
if __name__ == "__main__":
    pass
#    print conta_campos(cur)
    extrai_dados(cur,  1000, 50)
