# -*- coding:utf-8 -*-
"""
cria visualizações em mapas 
@Autor: Flávio
"""
from sqlalchemy.ext.sqlsoup import SqlSoup
from matplotlib.colors import rgb2hex
from matplotlib import cm
from kmlgen import EstadosAnimados

confs = "Flavio"

if confs == "Flavio":
    ubiServer = "http://10.250.46.208:20738/RPC2"
    MySQLServer = "mysql://root:password@E04324"

if confs == "Pablo":
    ubiServer = "http://127.0.0.1:20738/RPC2"
    MySQLServer = "mysql://pablo:pablo@E04324.fgv.br"
    
def mapa_processos():
    Q =dbsupremo.execute("""SELECT origem_sigla,DATE_FORMAT(data_entrada,'%Y') ano, COUNT(id) FROM t_processos
    WHERE (proc_class='AI' OR proc_class='RE') and (origem_sigla not like '%*%') AND (origem_sigla not like '%-%') AND (DATE_FORMAT(data_entrada,'%Y')>1900)
    GROUP BY origem_sigla,ano""")
    res = Q.fetchall()
    EA = EstadosAnimados('estados.kml')
    EA.add_data(res)
    EA.save('recursos.kml')


if __name__=="__main__":
    dbgrafo = SqlSoup("%s/SEN_Grafo" % MySQLServer)
    dbsupremo =  SqlSoup("%s/Supremo_new" % MySQLServer)
    dbdec = SqlSoup("%s/STF_Analise_Decisao" % MySQLServer)
    mapa_processos()
