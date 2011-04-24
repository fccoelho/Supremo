/* 
Autor: Pablo Cerdeira

Criando tabela única de relacionamento entre artigos, leis e decisões.
*/

/*
Primeiro vamos criar uma tabela em branco com a estrutura dos campos da artigo_lei
Não inserimos conteúdo ainda para podermos inserir depois, com uma PK.
*/
USE SEN_Grafo;

DROP TABLE IF EXISTS artigo;
CREATE TABLE artigo
SELECT 
  lei_id, numero artigo, count(numero) ocorrencias
FROM `STF_Analise_Decisao`.`artigo_lei`
WHERE 1 = 2;

/*
Inserindo coluna de id (PK) na tabela artigo.
*/
ALTER TABLE artigo 
    ADD COLUMN id INT NOT NULL AUTO_INCREMENT FIRST, 
    ADD PRIMARY KEY (id);

/*
Inserindo conteúdo na tabela artigo.
*/
INSERT INTO artigo (lei_id, artigo, ocorrencias) 
SELECT 
  lei_id, numero artigo, count(numero) ocorrencias
FROM `STF_Analise_Decisao`.`artigo_lei`
GROUP BY lei_id, numero
ORDER BY count(numero) DESC;