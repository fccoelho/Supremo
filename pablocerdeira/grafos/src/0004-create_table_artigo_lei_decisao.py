# -*- coding:utf-8 -*-
'''
Script para criar e popular a tabela de relacionamento
artigo_lei_decisao

Tabela artigo_lei_decisao
    Armazenamento de todas as relações entre artigos, leis
    e decisões.
    Colunas:
        id: pk autoincrement
        artigo_id: id do artigo na tabela artigo
        lei_id: id da lei na tabela lei
        decisao_id: coluna decisao_id da tabela lei_decisao

Autores:
    Pablo Cerdeira
    Flávio Coelho
    
Notas:
    - v0.1:
        Cria e popula tabela artigo_lei_decisao.

'''
import MySQLdb

conn = MySQLdb.connect (host = "E04324.fgv.br", 
                        user = "pablo",
                        passwd = "pablo",
                        db = "SEN_Grafo"
                        )
   
cursor1 = conn.cursor()

'''
Script para dropar e criar a tabela artigo_lei_decisao
'''
print "Dropando a tabela artigo_lei_decisao se ela existir"
sqlstr = '''
DROP TABLE IF EXISTS artigo_lei_decisao;
'''
cursor1.execute(sqlstr)


print "Criando a tabela artigo_lei_decisao"
sqlstr = '''
CREATE TABLE artigo_lei_decisao (
  id INT NOT NULL AUTO_INCREMENT,
  artigo_id INT(21) NULL,
  lei_id INT(21) NULL,
  decisao_id INT(21),
  PRIMARY KEY (id) );
'''
cursor1.execute(sqlstr)
print "Concluída a criação da tabela artigo_lei_decisao."


print "Alimentando a tabela artigo_lei_decisao..."

sqlstr = '''
INSERT INTO artigo_lei_decisao (artigo_id, lei_id, decisao_id) 
SELECT 
  a.id artigo_id,
  ld.lei_id lei_id,
  ld.decisao_id decisao_id
FROM 
  artigo a,
  lei_decisao ld,
  temp_artigo_lei al
where 
  ld.id = al.lei_id AND
  ld.lei_id = a.lei_id AND
  a.artigo = al.numero
''' 
cursor1.execute(sqlstr)


print "Criando índices na tabela artigo_lei_decisao."

sqlstr = '''
ALTER TABLE artigo_lei_decisao
    ADD INDEX ix_artigo_id (artigo_id ASC), 
    ADD INDEX ix_lei_id (lei_id ASC),
    ADD INDEX ix_decisao_id (decisao_id ASC);
''' 
cursor1.execute(sqlstr)


print "Concluído."

cursor1.close()
conn.close()
