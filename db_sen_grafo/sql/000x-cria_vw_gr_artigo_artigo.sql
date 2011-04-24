create view vw_gr_artigo_artigo as 
select graa.edge_id, 
  graa.artigo_id_1, a_1.artigo artigo_1, graa.lei_id_1, l_1.esfera esfera_1, l_1.lei lei_1, l_1.ano ano_1, 
  graa.artigo_id_2, a_2.artigo artigo_2, graa.lei_id_2, l_2.esfera esfera_2, l_2.lei lei_2, l_2.ano ano_2,
  graa.peso, graa.artigo_count
from 
  gr_artigo_artigo graa,
  artigo a_1,
  artigo a_2,
  lei l_1,
  lei l_2
where 
  graa.lei_id_1 = l_1.id and
  graa.lei_id_2 = l_2.id and
  graa.artigo_id_1 = a_1.id and
  graa.artigo_id_2 = a_2.id
order by graa.edge_id
