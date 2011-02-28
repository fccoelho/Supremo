"""
Modulo para criar Tabela e salvar dados de decisoes do subremo
"""
from elixir import *


metadata.bind = "mysql://root:password@E04324/STF_Analise_Decisao"
metadata.bind.echo = True

class SalvaNoBanco:
    """
    Salva os dados no banco
    """
    def __init__(self):
        self.esferas = {'LEG-FED': 'federal', 
                                'LEG-EST': 'estadual', 
                                'LEG-MUN':'municipal', 
                                'LEG-DIS':'distrital', 
                                'LEG-INT':'internacional'}
    def parse_partes_leis(self, D, L):
        """
        Parseia as partes das leis citadas, cria os registros
        no banco e retorna as instancias criadas
        """
        #determina esfera
        esfera = self.esferas[L[0]]
        lei = L[1]
        ano = L[2] if L[2].startswith('ANO') else None
        
        for i in L[3:]:
            if i.startswith('ART'):
                pass
            
        
    def salvar(self, decisao, datadec, datapub, tipo, processo, UF, leisjson):
        """
        salva no banco 
        """
        D = Decisao(processo=processo, tipo=tipo, data_dec=datadec, data_pub=datapub, UF=UF)
        for k, v in leisjson.iteritems(): #itera sobre as esferas citadas: Federal, Estadual, etc
            for l in v: # Itera sobre as leis citadas na dada esfera.
                self.parse_partes_leis(D, l)
        session.commit()

#===Modelos===

class Decisao(Entity):
    using_options(tablename='decisao')
    processo = Field(Integer, primary_key=True)
    tipo = Field(Unicode(45))
    data_dec = Field(Date)
    data_pub = Field(Date)
    UF = Field(Unicode(2))
    legislacao = OneToMany('Lei')
    def __repr__(self):
        return '<Decisao "%s" (%d)>' % (self.processo, self.data)
        
class Lei(Entity):
    using_options(tablename='lei_decisao')
    esfera = Field(Unicode(10))
    lei = Field(Unicode(16))
    ano = Field(Integer)
    decisoes = ManyToOne('Decisao')
    artigos = OneToMany('Artigo')
    

class Artigo(Entity):
    using_options(tablename='artigo_lei')
    lei = ManyToOne('Lei')
    numero = Field(Integer)
    paragrafos = OneToMany('Paragrafo')
    incisos = OneToMany('Inciso')
    
class Paragrafo(Entity):
    using_options(tablename='paragrafo_artigo')
    artigo = ManyToOne('Artigo')
    numero = Field(Integer)
    
class Inciso(Entity):
    using_options(tablename='inciso_artigo')
    artigo = ManyToOne('Artigo')
    numero = Field(Integer)
    letras = OneToMany('Letra')
    
class Letra(Entity):
    using_options(tablename='letra_inciso')
    inciso  = ManyToOne('Inciso')
    numero = Field(Integer)
    
    
if __name__=="__main__":
    setup_all(create_tables=True)
    create_all()
