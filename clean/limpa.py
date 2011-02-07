import difflib
#from sqlalchemy.ext.sqlsoup import SqlSoup
from BeautifulSoup import BeautifulSoup
#db = SqlSoup('mysql://root:password@emapserv/Supremo')
#print db.t_decisoes.all()
import MySQLdb
db=MySQLdb.connect(host="emapserv", user="root", passwd="password",db="Supremo")
cur=db.cursor()


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
    
    
if __name__ == "__main__":
    print conta_campos(cur)        
