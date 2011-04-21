/*
Testando a geração de uma query que retorna o mesmo
resultado da tabela SEN_Grafo.artigo_lei_decisao.

Funcionou! Levou 70 segundos, mas funcionou.
Parece que essa matrix pode ser usada como base para 
criação dos grafos.
*/
SELECT DISTINCT 
  id_processo, id_decisao, lei_id_artigo, artigo_id
FROM 
  SEN_Grafo.matrix
WHERE
  lei_id_artigo IS NOT NULL OR
  artigo_id IS NOT NULL
ORDER BY
  id_decisao;


/*
Segundo teste.
Fazendo query que deve gerar uma semelhante à
lei_decisao.
Funcionou também, como esperado.
*/
SELECT DISTINCT 
  id_processo, id_decisao, lei_id
FROM 
  SEN_Grafo.matrix
WHERE
  lei_id_artigo IS NOT NULL OR
  artigo_id IS NOT NULL
ORDER BY
  id_decisao;