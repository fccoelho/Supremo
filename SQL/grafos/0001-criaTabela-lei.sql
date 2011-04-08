/* 
Autor: Pablo Cerdeira

Criando tabela única de leis com base no conteúdo da tabela lei_decisao

Para isso realizamos um select distinct dos campos esfera, lei e ano
da tabela lei_decisao e ordenamos pelo count(ano) desc para deixar as leis
meis citadas no início da tabela.
*/

/*
Primeiro vamos criar uma tabela em branco com a estrutura dos campos da lei_decisao
Não inserimos conteúdo ainda para podermos inserir depois, com uma PK.
*/
CREATE TABLE lei
SELECT DISTINCT
    esfera, lei, ano
FROM
    lei_decisao
WHERE 
    1 <> 1
GROUP BY
    esfera, lei, ano
ORDER BY 
    count(ano) DESC;

/*
Inserindo coluna de id (PK) e codigo_correto na tabela lei.
O codigo_correto serve para receber o id de outra lei quando detectarmos erros de digitação
Adicionando índice.
*/
ALTER TABLE lei 
    ADD COLUMN id INT NOT NULL AUTO_INCREMENT FIRST, 
    ADD COLUMN id_correto INT NULL AFTER ano, 
    ADD PRIMARY KEY (id);

/*
Inserindo conteúdo na tabela lei.
*/
INSERT INTO lei (esfera, lei, ano) 
SELECT DISTINCT
    esfera, lei, ano
FROM
    lei_decisao
GROUP BY
    esfera, lei, ano
ORDER BY 
    count(ano) DESC;

/*
A busca por leis cadastradas de forma incorreta foi feita manualmente.
Inserimos o valor 1 na coluna id_correto em todos os casos que detecamos
que a constituição apresentada não existia.
*/
