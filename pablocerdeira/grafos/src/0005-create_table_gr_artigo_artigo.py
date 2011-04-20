# -*- coding:utf-8 -*-
'''
Script para criar e popular a tabela gr_artigo_artigo
Tabela gr_artigo_artigo
    Colunas:
        edge_id: pk autoincrement
        artigo_id_1: id do artigo na tabela artigo
        lei_id_1: id da lei na tabela artigo e na tabela lei
        artigo_id_2: id do artigo na tabela artigo
        lei_id_2: id da lei na tabela artigo e na tabela lei
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
  artigo_id_2 INT(21) NULL,
  lei_id_2 INT(21) NULL,
  peso INT(21) NULL ,
  artigo_count INT NULL ,
  PRIMARY KEY (edge_id) );
'''
cursor1.execute(sqlstr)
print "Concluída a criação da tabela."

'''
Criando índices
'''
print "Criando índices para a tabela."
sqlstr = '''
ALTER TABLE gr_artigo_artigo 
    ADD INDEX ix_artigo_id_1 (artigo_id_1 ASC),
    ADD INDEX ix_lei_id_1 (lei_id_1 ASC),
    ADD INDEX ix_artigo_id_2 (artigo_id_2 ASC),
    ADD INDEX ix_lei_id_2 (lei_id_2 ASC),
    ADD INDEX ix_peso (peso ASC),
    ADD INDEX ix_artigo_count (artigo_count ASC);
'''
cursor1.execute(sqlstr)
print "Concluída a criação dos índices."

'''
'''
print "Pegando o id de cada uma dos artigos e sua lei_id..."
sqlstr = "select id, lei_id from artigo order by id"
cursor1.execute(sqlstr)
print "Ok, ids e lei_ids dos artigos em memória..."

'''
Loop executado uma vez para cada id da tabela artigo detectado.
'''
print "Iniciando a montagem das queries em memória..."
i = 1
sqlstr = ""
while i < cursor1.rowcount-1:
    artigo_id_1, lei_id_1 = cursor1.fetchone()
    '''
    Inserindo um teste para lei_id_1 = None, pois isso estava gerando erro no
    script SQL.
    '''
    if lei_id_1 is None:
        lei_id_1 = "Null"
    sqlstr = sqlstr + '''
        insert into gr_artigo_artigo (artigo_id_1, lei_id_1, artigo_id_2, lei_id_2, peso) 
        select 
            %s artigo_id_1,
            %s lei_id_1,
            ld_1.artigo_id artigo_id_2,
            ld_1.lei_id lei_id_2,
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
                    ald_2.artigo_id = %s
            ) and 
            ld_1.artigo_id > %s
        group by ld_1.artigo_id 
        order by count(ld_1.artigo_id) desc;
        ''' % (str(artigo_id_1), str(lei_id_1), str(artigo_id_1),str(artigo_id_1))

    print "Inserindo artigo_id = %s na query" % str(artigo_id_1)
    # cursor2.execute(sqlstr)
    i += 1
    
print "Montagem da SqlStr concluída"
print "Iniciando o send da query (pode levar horas... vá buscar um café, um sanduíche, tomar um banho...)"
cursor2.execute(sqlstr)

f = open('strsql.sql','w')
f.write(sqlstr)
f.close

print '''
    Concluído no Python. 
    Provavelmente ainda está rodando no servidor MySQL.
    A execução no lado do servidor levará algumas horas ainda.
    Verifique a conclusão rodando o comando 'show processlist'
    
    Para saber qual a porcentagem dos artigos já inseridos na
    tabela gr_artigo_artigo execute o seguinte script no MySQL:
    
    SELECT max(graa.artigo_id_1)/max(a.id)*100 
    FROM artigo a, gr_artigo_artigo graa
    '''

cursor1.close()
cursor2.close()
conn.close()
