/* 
Autor: Pablo Cerdeira

Insere alguns id_correto na tabela lei

NOTA: este script precisa ser incrementado. Foi feita a comparação
apenas para os casos de Constituição cadastrada de forma incorreta.
É precido fazer para outras leis relevantes também.
*/

/*
Inserindo id_correto para os casos da Constituição 1988 detectados no banco.
Este trabalho é manual.
*/
UPDATE lei SET id_correto = 1
WHERE
	(
		esfera = "LEG-EST" AND
		lei = "CF" AND
		ano = 0
	) OR
	(
		esfera = "LEG-FED" AND
		lei = "CF" AND
		ano = 0
	) OR
	(
		esfera = "LEG-FED" AND
		lei = "CF" AND
		ano = 1998
	) OR
	(
		esfera = "LEG-EST" AND
		lei = "CF" AND
		ano = 1989
	) OR
	(
		esfera = "LEG-INT" AND
		lei = "CF" AND
		ano = 1988
	) OR
	(
		esfera = "outras" AND
		lei = "CF" AND
		ano = 1988
	);


/*
Inserindo id_correto para os casos da Constituição 1967 detectados no banco.
Este trabalho é manual.
*/
UPDATE lei SET id_correto = 29
WHERE
	(
		esfera = "LEG-FED" AND
		lei = "CF" AND
		ano = 1965
	);

/*
Inserindo id_correto para os casos da Constituição 1937 detectados no banco.
Este trabalho é manual.
*/
UPDATE lei SET id_correto = 99
WHERE
	(
		esfera = "LEG-FED" AND
		lei = "CF" AND
		ano = 1947
	);


