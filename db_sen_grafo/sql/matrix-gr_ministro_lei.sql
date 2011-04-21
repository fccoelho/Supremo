/*
Cria tabela gr_ministro_lei
*/
USE SEN_Grafo;

DROP TABLE IF EXISTS gr_ministro_lei;

CREATE TABLE
  gr_ministro_lei 
SELECT 
  relator origid, lei_id destid, count(lei_id) weight
FROM
  (
  SELECT DISTINCT 
    id_processo, relator, id_decisao, lei_id
  FROM 
    SEN_Grafo.matrix
  ) t
GROUP BY
  t.relator
ORDER BY
  count(t.lei_id) DESC;