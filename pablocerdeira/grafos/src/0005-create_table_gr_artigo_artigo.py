# -*- coding:utf-8 -*-
'''
Script para criar e popular a tabela gr_artigo_artigo
Tabela gr_artigo_artigo
    Colunas:
        edge_id: pk autoincrement
        artigo_id_1: id do artigo na tabela artigo
        lei_id_1: id da lei na tabela artigo e na tabela lei
        artigo_1: artigo na tabela artigo
        artigo_id_2: id do artigo na tabela artigo
        lei_id_2: id da lei na tabela artigo e na tabela lei
        artigo_2: artigo na tabela artigo
        peso: quantidade de decisões que citam os dois artigos
        artigo_count: indica qual a ordem do peso, para cada grupo 
            de relações artigo_id_1 <-> artigo_id_n (será preenchido 
            depois) 

Autores:
    Pablo Cerdeira
    Flávio Coelho
    
Notas:
    - v0.1:

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
Script para dropar se necessário e criar a tabela gr_artigo_artigo
'''
print "Dropando a tabela gr_artigo_artigo se ela existir"
sqlstr = '''
DROP TABLE IF EXISTS gr_artigo_artigo;
'''
cursor1.execute(sqlstr)
print "Criando a tabela gr_artigo_artigo"
sqlstr = '''
CREATE  TABLE gr_artigo_artigo (
  edge_id INT NOT NULL AUTO_INCREMENT ,
  artigo_id_1 INT(21) NULL,
  lei_id_1 INT(21) NULL,
  artigo_1 VARCHAR(45) NULL,
  artigo_id_2 INT(21) NULL,
  lei_id_2 INT(21) NULL,
  artigo_2 VARCHAR(45) NULL,
  peso INT(21) NULL ,
  artigo_count INT NULL ,
  PRIMARY KEY (edge_id) );
'''
cursor1.execute(sqlstr)
print "Concluída a criação da tabela."

'''
'''
print "Pegando o id de cada uma dos artigos..."
sqlstr = "select id from artigo order by id"
cursor1.execute(sqlstr)
print "Ok, ids dos artigos em memória..."

'''
Loop executado uma vez para cada id da tabela artigo detectado.
'''
print "Iniciando a montagem das queries em memória..."
i = 1
sqlstr = ""
while i < cursor1.rowcount-1:
    lei_id_1 = cursor1.fetchone()
    sqlstr = sqlstr + '''
select 
    1 artigo_id_1,
    1 lei_id_1,
    "00005" artigo_1,
    ld_1.artigo_id artigo_id_2,
    ld_1.lei_id lei_id_2,
    "Z" artigo_2,
    count(ld_1.artigo_id) peso 
from 
    artigo_lei_decisao ld_1 
where 
    ld_1.decisao_id in (
        select 
            ald_2.decisao_id 
        from 
            artigo_lei_decisao ald_2 
        where 
            ald_2.lei_id = 1 and
            ald_2.artigo_id = 1
    ) and 
    ld_1.artigo_id > 1
group by ld_1.artigo_id 
order by count(ld_1.artigo_id) desc; 
        ''' % (str(i), str(i), str(i))
    print "Inserindo lei_id = %s na query" % str(i)
    # cursor2.execute(sqlstr)
    i += 1
    
print "Montagem da SqlStr conclu�da"
print "Iniciando o send da query (pode levar horas... v� buscar um caf�...)"
cursor2.execute(sqlstr)
print '''
    Conclu�do no Python. 
    Provavelmente ainda est� rodando no servidor MySQL.
    A execu��o no lado do servidor levar� aproximadamente 1 hora ainda.
    Verifique a conclus�o rodando o comando 'show processlist'
    '''

cursor1.close()
cursor2.close()
conn.close()
