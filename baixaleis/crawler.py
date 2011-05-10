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
        pos = doc.find('</p>', pos)
    
    elif tag == '>TÍTULO':
        titulo += 1
        capitulo, secao, subsecao = 0, 0, 0
        pos = doc.find('</p>', pos)
    
    elif tag == '>CAPÍTULO':
        capitulo += 1
        secao, subsecao = 0, 0
        pos = doc.find('</p>', pos)
    
    elif tag == '>SEÇÃO':
        secao += 1
        subsecao = 0
        pos = doc.find('</p>', pos)
    
    elif tag == '>Subseção':
        subsecao += 1
        pos = doc.find('</p>', pos)
    
    elif tag[:3] == 'Art':
        artigo += 1
        idt += 1
        subartigo, inciso, paragrafo = 0, 0, 0
        t = get_text(doc, pos)
        g.writerow([idt, livro, titulo, capitulo, secao, subsecao, artigo,
                    subartigo, paragrafo, inciso, alinea, t])
        pos = doc.find('</p>', pos)
    
    elif tag == 'SubArtigo':
        i = pos
        tmp = ''
        while doc[i] != '-':
            if doc[i] in '0987654321':
                tmp += doc[i]
            i += 1
        if int(tmp) != artigo:
            artigo = int(tmp)
        
        subartigo += 1
        idt += 1
        inciso, paragrafo = 0, 0
        t = get_text(doc, pos)
        g.writerow([idt, livro, titulo, capitulo, secao, subsecao, artigo,
                    subartigo, paragrafo, inciso, alinea, t])
        pos = doc.find('</p>', pos)
    
    elif tag == 'Parágrafo':
        paragrafo += 1
        idt += 1
        inciso, alinea = 0, 0
        t = get_text(doc, pos)
        g.writerow([idt, livro, titulo, capitulo, secao, subsecao, artigo,
                    subartigo, paragrafo, inciso, alinea, t])
        pos = doc.find('</p>', pos)
    
    elif tag == 'Inciso':
        inciso += 1
        idt += 1
        alinea = 0
        t = get_text(doc, pos)
        g.writerow([idt, livro, titulo, capitulo, secao, subsecao, artigo,
                    subartigo, paragrafo, inciso, alinea, t])
        pos = doc.find('</p>', pos)
    
    elif tag == 'Alinea':
        alinea += 1
        idt += 1
        t = get_text(doc, pos)
        g.writerow([idt, livro, titulo, capitulo, secao, subsecao, artigo,
                    subartigo, paragrafo, inciso, alinea, t])
        pos = doc.find('</p>', pos)
    
    l = get_next_tag(doc, pos)
    print idt
