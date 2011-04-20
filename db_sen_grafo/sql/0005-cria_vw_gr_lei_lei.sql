create or replace view vw_gr_lei_lei as 
select grll.edge_id, 
  grll.lei_id_1, l_1.esfera esfera_1, l_1.lei lei_1, l_1.ano ano_1, 
  		 l_1.lei_nome lei_nome_1, l_1.lei_descricao lei_descricao_1, l_1.lei_tipo lei_tipo_1,
  grll.lei_id_2, l_2.esfera esfera_2, l_2.lei lei_2, l_2.ano ano_2, 
  		 l_2.lei_nome lei_nome_2, l_2.lei_descricao lei_descricao_2, l_2.lei_tipo lei_tipo_2,
  grll.peso, grll.lei_count
from 
  gr_lei_lei grll,
  lei l_1,
  lei l_2
where 
  grll.lei_id_1 = l_1.id and
  grll.lei_id_2 = l_2.id
order by grll.edge_id
