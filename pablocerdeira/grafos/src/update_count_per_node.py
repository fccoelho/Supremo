# -*- coding:utf-8 -*-
import MySQLdb

conn = MySQLdb.connect (host = "E04324.fgv.br", 
                        user = "pablo",
                        passwd = "pablo",
                        db = "SEN_Grafo"
                        )
   
cursor = conn.cursor()

conn2 = MySQLdb.connect (host = "E04324.fgv.br", 
                        user = "pablo",
                        passwd = "pablo",
                        db = "SEN_Grafo"
                        )

cursor2 = conn2.cursor()

cursor.execute("select edge_id, lei_id_1, lei_id_2, count_lei from gr_lei_lei")

print "Iniciando fetch"
i = 0
j = 1
lei_atual = lei_antiga = 0

while i < cursor.rowcount-2:
    id, lei_1, lei_2,c = cursor.fetchone()
    lei_atual = lei_1
    if lei_atual != lei_antiga:
        lei_antiga = lei_atual
        j = 1
        # print i, "Lei id 1: ", lei_1, "Lei id 2", lei_2
        sqlstr = "update gr_lei_lei set count_lei = %s where edge_id = %s"%(str(j),str(id))
        print sqlstr
        '''
        A linha abaixo executa, mas trava o script. 
        A execução fica travada no MySQLdb/cursors.py linha 282.
        282 > self._do_get_result()
        Por alguma razão quando ele executa a query ele fica travado.
        Deve ser algum bug no meu MySQLdb.
        Flávio, você poderia tentar rodar por ai, por favor?
        ''' 
        cursor2.execute(sqlstr)
    else:
        j += 1
        # print i, "Lei id 1: ", lei_1, "Lei id 2", lei_2
        sqlstr = "update gr_lei_lei set count_lei = %s where edge_id = %s"% (str(j),str(id))
        print sqlstr
        cursor2.execute(sqlstr)
    i += 1

cursor.close()

conn.close()
