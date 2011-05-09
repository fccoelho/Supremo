# -*- coding:utf-8 -*-

import csv
from utils import get_next_tag, get_text

f = open('codigo_processo_civil.htm', 'r')
g = csv.writer(open('codigo_processo_civil.csv', 'w'))

g.writerow(["'id'","'livro'","'titulo'","'capitulo'","'secao'",
            "'subsecao'","'artigo'","'paragrafo'","'inciso'",
            "'alinea'","'texto'"])

doc = ''
for line in f:
    doc += line

idt = 0
livro, titulo, capitulo, secao, subsecao = 0, 0, 0, 0, 0
artigo, paragrafo, inciso, alinea = 0, 0, 0, 0

l = get_next_tag(doc)

while l != []:    
    tag, pos = l[0], l[1]
    
    if tag == '>LIVRO':
        livro += 1
        titulo = 0
        pos += 1
    
    elif tag == '>TÍTULO':
        titulo += 1
        capitulo = 0
        pos += 1
    
    elif tag == '>CAPÍTULO':
        capitulo += 1
        secao = 0
        pos += 1
    
    elif tag == '>SEÇÃO':
        secao += 1
        subsecao = 0
        pos += 1
    
    elif tag == '>Subseção':
        subsecao += 1
        pos += 1
    
    elif tag == 'Art.':
        artigo +=1
        idt += 1
        inciso = 0
        paragrafo = 0
        t = get_text(doc, pos)
        g.writerow([idt, livro, titulo, capitulo, secao, subsecao, artigo,
                    paragrafo, inciso, alinea, t])
        pos += 1
    
    elif tag == 'Parágrafo':
        paragrafo += 1
        idt += 1
        inciso = 0
        t = get_text(doc, pos)
        g.writerow([idt, livro, titulo, capitulo, secao, subsecao, artigo,
                    paragrafo, inciso, alinea, t])
        pos += 1
    
    elif tag == 'Inciso':
        inciso += 1
        idt += 1
        paragrafo = 0
        alinea = 0
        t = get_text(doc, pos)
        g.writerow([idt, livro, titulo, capitulo, secao, subsecao, artigo,
                    paragrafo, inciso, alinea, t])
        pos += 1
    
    elif tag == 'Alinea':
        alinea += 1
        idt += 1
        t = get_text(doc, pos)
        g.writerow([idt, livro, titulo, capitulo, secao, subsecao, artigo,
                    paragrafo, inciso, alinea, t])
        pos += 1
    
    l = get_next_tag(doc, pos)
    print idt
