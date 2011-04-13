# -*- coding:utf-8 -*-
'''
Script para criar e popular a tabela artigo
Tabela artigo
    Responsável por armazenar os artigos de todas
    as leis citadas nas decisões do STF.
    Colunas:
        id: pk autoincrement
        lei_id: id da lei na tabela lei
        artigo: artigo da lei_id
        ocorrencias: quantidade de ocorrencias nas
        decisões. Este número não é para relacionamentos
        mas sim para termos uma ordem de importância 
        armazenada junto aos dados, para posterior limpeza. 

Autores:
    Pablo Cerdeira
    Flávio Coelho
    
Notas:
    - v0.1:
        Cria e popula tabela artigo na intância SEN_Grafo
        ATENÇÃO: Notar que a tabela artigo fica com alguns
        lei_id NULL. Isso se deve a problemas no preenchimento
        da tabela lei. Ver com Flávio.
        A criação da tabela temp_artigo_lei só é necessária
        porque meu usuário não tem permissão de alterar tabelas
        na STF_Analise_Decisao.

'''
import MySQLdb

conn = MySQLdb.connect (host = "E04324.fgv.br", 
                        user = "pablo",
                        passwd = "pablo",
                        db = "SEN_Grafo"
                        )
   
cursor1 = conn.cursor()

'''
Script para dropar se necessário e criar a tabela artigo
'''
print "Dropando a tabela artigo se ela existir"
sqlstr = '''
DROP TABLE IF EXISTS artigo;
'''
cursor1.execute(sqlstr)


print "Dropando a tabela temp_artigo_lei se ela existir"
sqlstr = '''
DROP TABLE IF EXISTS temp_artigo_lei;
'''
cursor1.execute(sqlstr)


print "Criando a tabela artigo"
sqlstr = '''
CREATE TABLE artigo (
  id INT NOT NULL AUTO_INCREMENT ,
  lei_id INT(21) NULL ,
  artigo VARCHAR(50) NULL ,
  ocorrencias INT(21) NULL ,
  PRIMARY KEY (id) );
'''
cursor1.execute(sqlstr)
print "Concluída a criação da tabela artigo."


print "Criando uma cópia da tabela artigo_lei na SEN_Grafo..."

sqlstr = '''
create table temp_artigo_lei 
select *
from 
  STF_Analise_Decisao.artigo_lei;
''' 
cursor1.execute(sqlstr)


print "Adicionando índices à tabela temp_artigo_lei..."

sqlstr = '''
ALTER TABLE temp_artigo_lei 
    ADD INDEX ix_id (id ASC), 
    ADD INDEX ix_lei_id (lei_id ASC),
    ADD INDEX ix_numero (numero ASC);
'''
cursor1.execute(sqlstr)


print "Fazendo o select insert para popular a tabela artigo..."

sqlstr = '''
insert into artigo (lei_id, artigo, ocorrencias) 
select ld.lei_id, numero artigo, count(numero) ocorrencias
from 
  lei_decisao ld,
  temp_artigo_lei al
where 
  al.lei_id = ld.id
group by
  ld.lei_id, numero
order by
  count(numero) desc;
''' 
cursor1.execute(sqlstr)


print "Criando índices na tabela artigo. Acredite, é necessário..."

sqlstr = '''
ALTER TABLE artigo 
    ADD INDEX ix_lei_id (lei_id ASC), 
    ADD INDEX ix_artigo (artigo ASC), 
    ADD INDEX ix_ocorrencias (ocorrencias ASC);
'''
cursor1.execute(sqlstr)


print "Concluído. Enjoy!"

cursor1.close()
conn.close()
