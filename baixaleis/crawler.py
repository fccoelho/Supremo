# -*- coding:utf-8 -*-

import csv
from utils import get_next_tag, get_text

f = open('codigo_processo_civil.htm', 'r')
g = csv.writer(open('codigo_processo_civil.csv', 'w'))

g.writerow(["'id'","'livro'","'titulo'","'capitulo'","'secao'",
            "'subsecao'","'artigo'", "'sub_artigo'", "'paragrafo'","'inciso'",
            "'alinea'","'texto'"])

doc = ''
for line in f:
    doc += line

idt = 0
livro, titulo, capitulo, secao, subsecao = 0, 0, 0, 0, 0
artigo, subartigo, paragrafo, inciso, alinea = 0, 0, 0, 0, 0

l = get_next_tag(doc)

while l != []:    
    tag, pos = l[0], l[1]
    
    if tag == '>LIVRO':
        livro += 1
        titulo = 0
        pos += len(tag)
    
    elif tag == '>TÍTULO':
        titulo += 1
        capitulo = 0
        pos += len(tag)
    
    elif tag == '>CAPÍTULO':
        capitulo += 1
        secao = 0
        pos += len(tag)
    
    elif tag == '>SEÇÃO':
        secao += 1
        subsecao = 0
        pos += len(tag)
    
    elif tag == '>Subseção':
        subsecao += 1
        pos += len(tag)
    
    elif tag[:4] == 'Art.':
        artigo +=1
        idt += 1
        subartigo, inciso, paragrafo = 0, 0, 0
        t = get_text(doc, pos)
        g.writerow([idt, livro, titulo, capitulo, secao, subsecao, artigo,
                    subartigo, paragrafo, inciso, alinea, t])
        pos += 1
    
    elif tag == 'SubArtigo':
        subartigo += 1
        idt += 1
        inciso, paragrafo = 0, 0
        t = get_text(doc, pos)
        g.writerow([idt, livro, titulo, capitulo, secao, subsecao, artigo,
                    subartigo, paragrafo, inciso, alinea, t])
        pos += 1
    
    elif tag == 'Parágrafo':
        paragrafo += 1
        idt += 1
        inciso, alinea = 0, 0
        t = get_text(doc, pos)
        g.writerow([idt, livro, titulo, capitulo, secao, subsecao, artigo,
                    subartigo, paragrafo, inciso, alinea, t])
        pos += len(tag)
    
    elif tag == 'Inciso':
        inciso += 1
        idt += 1
        alinea = 0
        t = get_text(doc, pos)
        g.writerow([idt, livro, titulo, capitulo, secao, subsecao, artigo,
                    subartigo, paragrafo, inciso, alinea, t])
        pos += len(tag)
    
    elif tag == 'Alinea':
        alinea += 1
        idt += 1
        t = get_text(doc, pos)
        g.writerow([idt, livro, titulo, capitulo, secao, subsecao, artigo,
                    subartigo, paragrafo, inciso, alinea, t])
        pos += len(tag)
    
    l = get_next_tag(doc, pos)
    print idt
