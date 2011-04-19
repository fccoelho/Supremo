# -*- coding:utf-8 -*-
"""
Modulo para criar Tabela e salvar dados de decisoes do subremo
"""
from elixir import ManyToOne, Date, Integer, OneToMany, Entity, using_options, Field, create_all, setup_all, metadata, session, Unicode
import json
import sys


metadata.bind = "mysql://root:password@E04324/STF_Analise_Decisao"
metadata.bind.echo = False

class SalvaNoBanco:
    """
    Salva os dados no banco
    """
    def __init__(self):
        self.outrasleis = set([])
        self.gabarito = {"esfera": ["LEG-INT", "LEG-FED", "LEG-EST","LEG-MUN","LEG-DIS", ], 
                                "lei": ["CF", "CF-", u"CONSTITUIÇÃO FEDERAL",  "EMC-", 
                                            "LEI-","LEI", 
                                            "RGI", "STF-",  "RISTF-",  "REGIMENTO INTERNO DO SUPREMO TRIBUNAL FEDERAL", 
                                            "CPP-", "CÓDIGO DE PROCESSO PENAL", 
                                            "CPC-",  u"CÓDIGO DE PROCESSO CIVIL", 
                                            "ADCT", "ADM", "ANT", "AVS", "AEX", "ADC", "ASR", "ATO", "AIT", "ACP", "ACT","ATR","ADN", 
                                            "CLT", "CTA", "CMS", "COM","CNV", "CVC","CIR","CES","CPM-",
                                            "PRT", "PRV", "PRS", "PRI","PRC", "PTR", "PRO", 
                                            "DEC", "DCT", "DLB", "DCO", "DLG","DLC", "DNT", "DEL-",
                                            "EMR", "EXM", "EDT", "EM", "ETT", "EE", "EMD", "EST", "ENA", "ECR", 
                                            "INT", "ICP",
                                            "LDL", "LCP", "LMS", "LI", "LU", "LEP",
                                            "MPR", "MMO", "MCR", "MSG", 
                                             "ON", "OJ", "OSV", "OFC", 
                                             "PRJ", "PJL", "PEC", "PRN", 
                                            "RCD", "RBC", "RAL", "RNT", "RAD", "RTE", "RJU", "RES", "REG", "RSF",
                                            "SUV", "SUM", 
                                            "TLX", "TRF","TTD" , 
                                            "UM",
                                            ], 
                        "ano": ["ANO-"], 
                        "artigo": ["ART-", "ATR", "CAPUT"],
                        "inciso": ["INC-"], 
                        "paragrafo": ["PAR-",u"PARÁGRAFO ÚNICO",  "PARAGRAFO UNICO"], 
                        "letra": ["LET-"]
                     }

    def parse_partes_leis(self, D, L):
        """
        Parseia as partes das leis citadas, cria os registros
        no banco e retorna as instancias criadas
        """
        
        #determina esfera
        esfera = L[0] if L[0] in self.gabarito['esfera'] else'outras'
        ano =0
        if esfera == 'outras':
            print "==> outras esferas :",  L[0]
        #lei = ""
        try:
            lei = L[1] if  sum((L[1].encode('utf8').startswith(i) for i in self.gabarito['lei']))>0 else None
            if not lei:
                if L[1].startswith('ANO-'):
                    try:
                        ano = int(L[1].split('-')[1])
                    except ValueError:
                        ano = 0
                else:
                    self.outrasleis.add(L[1].split('-')[0])
        except IndexError: #caso em que lei nao esta especificada
            lei = L[0]

        try:
            ano = int(L[2].split('-')[1]) if sum((L[2].startswith(i) for i in self.gabarito['ano']))>0 else 0
        except IndexError:#caso em que ano nao esta especificado
            ano = ano if ano else 0
        except ValueError:
            ano = 0
        LEI = Lei(esfera=esfera, lei=lei, ano=ano, decisao=D)
        if  len(L) <3:
            return
        a=inc=None
        for i in L[3:]:
            i = i.strip(',')
            try:
                if sum((i.startswith(j) for j in self.gabarito['artigo']))>0:
                    a = Artigo(lei=LEI, numero=i.split('-')[1])
                elif sum((i.startswith(j) for j in self.gabarito['paragrafo']))>0:
                    if not a: a=None
                    p= Paragrafo(artigo=a, numero=i)
                elif i.startswith('INC-'):
                    if not a: a=None
                    inc = Inciso(artigo=a, numero=i.split('-')[1])
                elif i.startswith('LET-'):
                    if not inc: inc=None
                    l = Letra(inciso=inc, letra=i.split('-')[1])
                else:
                    pass
#                    print i
            except ValueError, e:
                print "ValueError: ", i, e
            except:
                print "Unexpected error:", sys.exc_info()[0]
        
    def salvar(self, datadec, datapub, tipo, processo, UF, leisjson, proc_classe, relator, duracao, origem, dec_id):
        """
        salva no banco 
        """
        leisjson = json.loads(leisjson.decode('iso-8859-1'))
#        print leisjson.items()
        D = Decisao(id=dec_id, processo=processo, tipo=tipo, data_dec=datadec, data_pub=datapub, 
                    UF=UF, proc_classe = proc_classe, relator=relator, duracao=duracao, origem=origem)
        for k, v in leisjson.iteritems(): #itera sobre as esferas citadas: Federal, Estadual, etc
            for l in v: # Itera sobre as leis citadas na dada esfera.
                self.parse_partes_leis(D, l)
            
    def commit_data(self):
        session.commit()

#===Modelos===

class Decisao(Entity):
    id = Field(Integer, primary_key=True,  required=True)
    using_options(tablename='decisao')
    processo = Field(Integer)
    tipo = Field(Unicode(45))
    proc_classe = Field(Unicode(128))
    relator = Field(Unicode(256))
    duracao = Field(Integer)
    origem = Field(Unicode(128))
    data_dec = Field(Date)
    data_pub = Field(Date)
    UF = Field(Unicode(2))
    legislacao = OneToMany('Lei')
    def __repr__(self):
        return '<Decisao "%s" (%s)>' % (self.processo, self.data_dec)
        
class Lei(Entity):
    using_options(tablename='lei_decisao')
    esfera = Field(Unicode(10))
    lei = Field(Unicode(32))
    ano = Field(Integer)
    decisao = ManyToOne('Decisao')
    artigos = OneToMany('Artigo')
    

class Artigo(Entity):
    using_options(tablename='artigo_lei')
    lei = ManyToOne('Lei')
    numero = Field(Unicode(32))
    paragrafos = OneToMany('Paragrafo')
    incisos = OneToMany('Inciso')
    
class Paragrafo(Entity):
    using_options(tablename='paragrafo_artigo')
    artigo = ManyToOne('Artigo')
    numero = Field(Unicode(128))
    
class Inciso(Entity):
    using_options(tablename='inciso_artigo')
    artigo = ManyToOne('Artigo')
    numero = Field(Unicode(32))
    letras = OneToMany('Letra')
    
class Letra(Entity):
    using_options(tablename='letra_inciso')
    inciso  = ManyToOne('Inciso')
    letra = Field(Unicode(16))

if __name__=="__main__":
    setup_all(create_tables=True)
    create_all()
