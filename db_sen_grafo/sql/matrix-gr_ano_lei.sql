/*
Cria tabela gr_ano_lei
*/
USE SEN_Grafo;

DROP TABLE IF EXISTS gr_ano_lei;

CREATE TABLE
  gr_ano_lei 
SELECT 
  t.ano origid, lei_id destid, count(lei_id) weight
FROM
  (
  SELECT DISTINCT 
    id_processo, year(data_decisao) ano, id_decisao, lei_id
  FROM 
    SEN_Grafo.matrix
  ) t
GROUP BY
  t.ano, t.lei_id
ORDER BY
  count(t.lei_id) DESC;