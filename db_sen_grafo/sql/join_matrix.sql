USE SEN_Grafo;
DROP TABLE IF EXISTS matrix;
CREATE TABLE matrix
SELECT
  p.id_processo,
  pcor.corte,
  p.proc_class,
  p.origem_sigla,
  p.origem_tribunal,
  p.relator,
  p.data_entrada,
  p.data_baixa,
  d.id id_decisao,
  d.data_decisao,
  pa.id_parte,
  pa.polo polo_parte,
  padv.id_advogado,
  padv.polo polo_advogado,
  ass.assunto,
  ass.sub_assunto1,
  ass.sub_assunto2,
  ass.sub_assunto3,
  ass.sub_assunto4,
  ass.sub_assunto5,
  ass.sub_assunto6,
  ld.lei_id lei_id,
  ald.lei_id lei_id_artigo,
  ald.artigo_id
FROM 
  (
    (
      (
        (
          (
            (
              Supremo_new.t_processos p
              LEFT JOIN
              Supremo_new.t_decisoes d
              ON p.id_processo = d.id_processo
            )
            LEFT JOIN
            Supremo_new.r_processos_partes pa
            ON p.id_processo = pa.id_processo
           )
          LEFT JOIN
          Supremo_new.r_processos_advogados padv
          ON p.id_processo = padv.id_processo
        )
        LEFT JOIN
        Supremo_new.r_processos_cortes pcor
        ON p.id_processo = pcor.id_processo
      )
      LEFT JOIN
      Supremo_new.t_assuntos ass
      ON p.id_processo = ass.id_processo
    )
    LEFT JOIN
    SEN_Grafo.lei_decisao ld
    ON d.id = ld.decisao_id
  )
    LEFT JOIN
    SEN_Grafo.artigo_lei_decisao ald
    ON d.id = ald.decisao_id AND ld.decisao_id = ald.decisao_id 
;

ALTER TABLE `SEN_Grafo`.`matrix` ENGINE = MariaDB; 

ALTER TABLE `SEN_Grafo`.`matrix`  
  ADD INDEX `ix_id_processo` (`id_processo` ASC) 
, ADD INDEX `ix_corte` (`corte` ASC) 
, ADD INDEX `ix_proc_class` (`proc_class` ASC) 
, ADD INDEX `ix_origem_tribunal` (`origem_tribunal` ASC) 
, ADD INDEX `ix_relator` (`relator` ASC) 
, ADD INDEX `ix_data_entrada` (`data_entrada` ASC) 
, ADD INDEX `ix_data_baixa` (`data_baixa` ASC) 
, ADD INDEX `ix_id_decisao` (`id_decisao` ASC) 
, ADD INDEX `ix_data_decisao` (`data_decisao` ASC) 
, ADD INDEX `ix_id_parte` (`id_parte` ASC) 
, ADD INDEX `ix_polo_parte` (`polo_parte` ASC) 
, ADD INDEX `ix_id_advogado` (`id_advogado` ASC) 
, ADD INDEX `ix_polo_advogado` (`polo_advogado` ASC) 
, ADD INDEX `ix_assunto` (`assunto` ASC) 
, ADD INDEX `ix_sub_assunto1` (`sub_assunto1` ASC) 
, ADD INDEX `ix_sub_assunto2` (`sub_assunto2` ASC) 
, ADD INDEX `ix_sub_assunto3` (`sub_assunto3` ASC) 
, ADD INDEX `ix_sub_assunto4` (`sub_assunto4` ASC) 
, ADD INDEX `ix_sub_assunto5` (`sub_assunto5` ASC) 
, ADD INDEX `ix_sub_assunto6` (`sub_assunto6` ASC) 
, ADD INDEX `ix_lei_id` (`lei_id` ASC) 
, ADD INDEX `ix_lei_id_artigo` (`lei_id_artigo` ASC) 
, ADD INDEX `ix_artigo_id` (`artigo_id` ASC) 
, ADD INDEX `ix_origem_sigla` (`origem_sigla` ASC) ;

