# -*- coding:utf-8 -*-
"""
Prepara logfiles a partir de series historicas de decisoes para visualizaçao com o programa Gource:
http://code.google.com/p/gource

para visualizar os logs use o sequinte comando:
$ gource --log-format custom decisoes_<ano>.log

ou para avançar mais rapido:

$ gource --log-format custom --seconds-per-day 1 custom decisoes_<ano>.log

Convem converter o arquivo gerado para utf-8 com

$ iconv -f iso-8859-1 -t utf-8 decisoes_1998.log > decisoes_1998_utf-8.log

para criar um video a partir da visualização (60 fps):

gource --log-format custom --seconds-per-day 1 custom decisoes_<ano>.log -o - | ffmpeg -y -r 60 -f image2pipe -vcodec ppm -i - -vcodec libvpx -b 10000K decisoes_<ano>.webm
"""

__author__="flavio"
__date__ ="$28/06/2011 15:40:23$"

from sqlalchemy.ext.sqlsoup import SqlSoup
from matplotlib.colors import rgb2hex
from matplotlib import cm
from matplotlib.colors import normalize
from collections import defaultdict
import numpy as np
import time
import datetime

MySQLServer = "mysql://root:password@E04324"

def db_to_logs(ano):
    """
    Extrai as decisoes do bancoe as salva em um arquivo no formato do Gource
    """
    #Q = dbdec.execute("SELECT relator,processo,tipo,proc_classe,duracao, UF,data_dec, count(*) FROM decisao WHERE DATE_FORMAT(data_dec,'%Y%')="+"%s"%ano+" GROUP BY relator,tipo,proc_classe")
    Q = dbdec.execute("SELECT relator,processo,tipo,proc_classe,duracao, UF,data_dec FROM decisao WHERE DATE_FORMAT(data_dec,'%Y%')="+"%s"%ano+" ORDER BY data_dec asc")
    decs = Q.fetchall()
    durations = [d[4] for d in decs]
    cmap = cm.jet
    norm = normalize(min(durations), max(durations)) #normalizing durations
    with open('decisoes_%s.log'%ano, 'w') as f:
        for d in decs:
            c = rgb2hex(cmap(norm(d[4]))[:3]).strip('#')
            path = "/%s/%s/%s/%s"%(d[5],d[2],d[3], d[1]) #/State/tipo/proc_classe/processo
            l = "%s|%s|%s|%s|%s\n"%(int(time.mktime(d[6].timetuple())), d[0], 'A', path, c)
            f.write(l)



if __name__ == "__main__":
    dbgrafo = SqlSoup("%s/SEN_Grafo" % MySQLServer)
    dbsupremo =  SqlSoup("%s/Supremo_new" % MySQLServer)
    dbdec = SqlSoup("%s/STF_Analise_Decisao" % MySQLServer)
    
    db_to_logs(1998)
