/* 
Autor: Pablo Cerdeira

Insere os valores de lei_id na tabela lei_decisao.

*/

/* 
Inserindo primeiro os valores de id da tabela lei, mesmo
que incorretos.
ATENÇÃO: se a tabela lei_decisao e a tabela lei estiverem
sem índices nas colunas esfera, lei e ano esta query é 
bastante demorada.
Por isso antes vamos inserir os índices em ambas.
*/
USE SEN_Grafo;


ALTER TABLE lei
      ADD INDEX ix_esfera (esfera ASC), 
      ADD INDEX ix_lei (lei ASC), 
      ADD INDEX ix_ano (ano ASC);

ALTER TABLE lei_decisao
      ADD INDEX ix_esfera (esfera ASC), 
      ADD INDEX ix_lei (lei ASC), 
      ADD INDEX ix_ano (ano ASC);

UPDATE
	lei_decisao ld,
	lei l
SET ld.lei_id = l.id
WHERE
	l.esfera = ld.esfera AND
	l.lei = ld.lei AND
	l.ano = ld.ano;

/*
Agora fazendo a atualização dos lei_id na tabela lei_decisao
para os casos em que a lei está incorretamente grafada.
Ou seja, pegamos os valores id_correto da tabela lei.
*/
UPDATE
	lei_decisao ld,
	lei l
SET ld.lei_id = l.id_correto
WHERE
	l.esfera = ld.esfera AND
	l.lei = ld.lei AND
	l.ano = ld.ano AND
	l.id_correto IS NOT NULL;

/*
ATENÇÃO: É importante criar os índices para para lei_decisao, 
do contrário a execução dos scripts em Python serão seriamente
afetadas.
*/
ALTER TABLE lei_decisao
      ADD INDEX ix_id (id ASC),
      ADD INDEX ix_decisao_id (decisao_id ASC),
      ADD INDEX ix_lei_id (lei_id ASC);

/*
Concluída esta etapa, o próximo passo é executar os scripts
Python disponíveis no diretório /pablocerdeira/grafos/src
*/
