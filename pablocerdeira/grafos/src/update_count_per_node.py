import MySQLdb
import MySQLdb.cursors
# o MySQLdb.cursor permite o uso de server side queries

conn = MySQLdb.connect (host = "E04324", 
                        user = "pablo",
                        passwd = "pablo",
                        db = "SEN_Grafo",
                        cursorclass = MySQLdb.cursors.SSCursor
                        )
   
cursor = conn.cursor()
cursor2 = conn.cursor()

cursor.execute("select edge_id, lei_id_1, lei_id_2 from gr_lei_lei limit 0,100000")

print "Iniciando fetch"
i = 0
j = 1
lei_atual = lei_antiga = cursor.fetchone()[0]

while (i < (cursor.rowcount-1)):
    id, lei_1, lei_2 = cursor.fetchone()
    lei_atual = lei_1
    if (lei_atual <> lei_antiga):
        lei_antiga = lei_atual
        j = 1
        print i, "Lei id 1: ", lei_1, "Lei id 2", lei_2
        sqlstr = "update gr_lei_lei set count_lei = ", j, "where edge_id = ", id
        print sqlstr
        # cursor2.execute(sqlstr)
    else:
        j += 1
        print i, "Lei id 1: ", lei_1, "Lei id 2", lei_2
        sqlstr = "update gr_lei_lei set count_lei = ", j, "where edge_id = ", id
        print sqlstr
        # cursor2.execute(sqlstr)
    i += 1

cursor.close()

conn.close()