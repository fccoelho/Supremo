# -*- coding:utf-8 -*-
"""
Modulo para criar Tabela e salvar dados de decisoes do subremo
"""
from elixir import *
import json
import sys


metadata.bind = "mysql://root:password@E04324/STF_Analise_Decisao"
metadata.bind.echo = False

class SalvaNoBanco:
    """
    Salva os dados no banco
    """
    def __init__(self):
        self.gabarito = {"esfera": ["LEG-INT", "LEG-FED", "LEG-EST","LEG-MUN","LEG-DIS", ], 
                                "lei": ["CF", "CF-", "CONSTITUIÇÃO FEDERAL",  "EMC-", 
                                            "LEI-",
                                            "RGI",  "STF-",  "RISTF-",  "REGIMENTO INTERNO DO SUPREMO TRIBUNAL FEDERAL", 
                                            "SUM-", 
                                            "DEL-",
                                            "CPP-",  "CÓDIGO DE PROCESSO PENAL", 
                                            "CPC-",  "CÓDIGO DE PROCESSO CIVIL", 
                                            "CPM-", 
                                            "ADCT", 
                                            "CLT"
                                            ], 
                        "ano": ["ANO-"], 
                        "artigo": ["ART-"],
                        "inciso": ["INC-"], 
                        "paragrafo": ["PAR-",  "PARÁGRAFO ÚNICO",  "PARAGRAFO UNICO", "CAPUT"], 
                        "letra": ["LET-"]
                     }

    def parse_partes_leis(self, D, L):
        """
        Parseia as partes das leis citadas, cria os registros
        no banco e retorna as instancias criadas
        """
        #determina esfera
        esfera = L[0] if L[0] in self.gabarito['esfera'] else'outras'
        try:
            lei = L[1] if  sum((L[1].startswith(i) for i in self.gabarito['lei']))>0 else None
        except IndexError: #caso em que lei nao esta especificada
            lei = L[0]
        try:
            ano = L[2] if sum((L[2].startswith(i) for i in self.gabarito['ano']))>0 else 0
        except IndexError:#caso em que ano nao esta especificado
            ano = 0
        if ano !=0:
            int(ano.split('-')[1])
        print D
        LEI = Lei(esfera=esfera, lei=lei, ano=ano, decisao=D)
        if  len(L) <3:
            return
        a=inc=None
        for i in L[3:]:
            i = i.strip(',')
            try:
                if i.startswith('ART'):
                    a = Artigo(lei=LEI, numero=int(i.split('-')[1]))
                elif sum((i.startswith(j) for j in self.gabarito['paragrafo']))>0:
                    if not a: a=None
                    p= Paragrafo(artigo=a, numero=int(i.split('-')[1]))
                elif i.startswith('INC-'):
                    if not a: a=None
                    inc = Inciso(artigo=a, numero=int(i.split('-')[1]))
                elif i.startswith('LET-'):
                    if not inc: inc=None
                    l = Letra(inciso=inc, letra=i.split('-')[1])
                else:
                    print i
            except ValueError:
                print "ValueError: ", i
            except:
                print "Unexpected error:", sys.exc_info()[0]
#        print LEI
        
    def salvar(self, datadec, datapub, tipo, processo, UF, leisjson):
        """
        salva no banco 
        """
        leisjson = json.loads(leisjson.decode('iso-8859-1'))
#        print leisjson.items()
        D = Decisao(processo=processo, tipo=tipo, data_dec=datadec, data_pub=datapub, UF=UF)
        for k, v in leisjson.iteritems(): #itera sobre as esferas citadas: Federal, Estadual, etc
            for l in v: # Itera sobre as leis citadas na dada esfera.
                self.parse_partes_leis(D, l)
    def commit_data(self):
        session.commit()

#===Modelos===

class Decisao(Entity):
    using_options(tablename='decisao')
    processo = Field(Integer)
    tipo = Field(Unicode(45))
    data_dec = Field(Date)
    data_pub = Field(Date)
    UF = Field(Unicode(2))
    legislacao = OneToMany('Lei')
    def __repr__(self):
        return '<Decisao "%s" (%s)>' % (self.processo, self.data_dec)
        
class Lei(Entity):
    using_options(tablename='lei_decisao')
    esfera = Field(Unicode(10))
    lei = Field(Unicode(16))
    ano = Field(Integer)
    decisao = ManyToOne('Decisao')
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
    letra = Field(String(1))
    
setup_all(create_tables=True)
create_all()
if __name__=="__main__":
    setup_all(create_tables=True)
    create_all()
