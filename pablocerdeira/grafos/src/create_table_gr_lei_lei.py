# -*- coding:utf-8 -*-
'''
Script para criar e popular a tabela gr_lei_lei

Tabela gr_lei_lei
    Responsável por armazenar as relações entre cada lei
    citada nas decisões do STF com as demais leis citadas 
    na mesma decisão.
    Colunas:
        edge_id: pk autoincrement
        lei_id_1: id da lei na tabela lei
        lei_id_2: id da lei relacionada na tabela lei
        peso: quantidade de decisões que citam as duas leis
        lei_count: indica qual a ordem do peso, para cada grupo 
            de relações lei_id_1 <-> lei_id_n (será preenchido 
            depois) 

Autores:
    Pablo Cerdeira
    Flávio Coelho

'''
import MySQLdb

conn = MySQLdb.connect (host = "E04324.fgv.br", 
                        user = "pablo",
                        passwd = "pablo",
                        db = "SEN_Grafo"
                        )
   
cursor1 = conn.cursor()
cursor2 = conn.cursor()

'''
Script para criar a tabela gr_lei_lei
'''
sqlstr = '''
CREATE  TABLE gr_lei_lei (
  edge_id INT NOT NULL AUTO_INCREMENT ,
  lei_id_1 INT(21) NULL ,
  lei_id_2 INT(21) NULL ,
  peso INT(21) NULL ,
  lei_count INT NULL ,
  PRIMARY KEY (edge_id) );
'''
cursor1.execute(sqlstr)

'''
Pega todos os lei_id da tabela lei que não tenham a coluna id_correto
preenchido (com id_correto significa que a lei está cadastrada com erro)
É importante pegar na ordem crescente para evitarmos referências duplicadas
na tabela final (lei_id_1 <-> lei_id_2 e lei_id_2 <-> lei_id_1). 
'''
sqlstr = "select id from lei order by id"
cursor1.execute(sqlstr)

'''
Loop executado uma vez para cada id da tabela lei detectado.
'''
i = 1
while i < cursor1.rowcount-1:
    lei_id_1 = cursor1.fetchone()
    sqlstr = '''
        insert into gr_lei_lei (lei_id_1, lei_id_2, peso) 
            select %s lei_id_1, ld_1.lei_id lei_id_2, count(ld_1.lei_id) peso 
            from lei_decisao ld_1 
            where 
                ld_1.decisao_id in (
                    select ld_2.decisao_id 
                    from lei_decisao ld_2 
                    where ld_2.lei_id = %s
                ) 
                and ld_1.lei_id > %s 
            group by ld_1.lei_id 
            order by count(ld_1.lei_id) desc;
        ''' % (str(i), str(i), str(i))
    print "Inserindo lei_id = %s" % str(i)
    cursor2.execute(sqlstr)
    i += 1

