# -*- coding:utf-8 -*-

import csv
from utils import get_next_tag

f = open('codigo_processo_civil.htm', 'r')
g = open('codigo_processo_civil.csv', 'r+')

g.write('"livro","título","capítulo","seção","subseção","artigo","inciso",
        "parágrafo","texto")

doc = ''
for line in f:
    doc += line

livro, titulo, capitulo, secao = 0, 0, 0, 0
subsecao, artigo, paragrafo, inciso, alinea = 0, 0, 0, 0, 0

l = get_next_tag(doc)

while l != []
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
        inciso = 0
        parágrafo = 
        t = get_text(pos)
        g.write('"%d","%d","%d","%d,"%d","%d","%d","%d",' %
                (livro, titulo, capitulo, secao, subsecao, artigo, inciso,
                 paragrafo) + '"' + t + '"')
        pos += 1
