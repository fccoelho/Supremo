/* 
Autor: Pablo Cerdeira

Importando tabela lei_decisao da instância STF_Analise_Decisao

*/

CREATE TABLE lei_decisao
SELECT *
FROM
    STF_Analise_Decisao.lei_decisao;

/*
Inserindo coluna de lei_id para informar qual o id único da lei a que
se refere a decisão.
*/
ALTER TABLE lei_decisao
    ADD COLUMN lei_id INT NULL AFTER decisao_id;
