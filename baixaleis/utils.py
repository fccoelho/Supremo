# -*- coding:utf-8 -*-

import re


def get_next_tag(string, inicio=0):
    r = []
    r.append(re.search('>LIVRO|>TÍTULO|>CAPÍTULO|>SEÇÃO|>Subseção|Art.*?[0-9]+[^0-9-]', string[inicio:]))
    r.append(re.search('Art\.[ \n][0-9]+-', string[inicio:]))
    r.append(re.search('[IVXLC]+[IVXLCl]*(&nbsp;| -)', string[inicio:]))
    r.append(re.search('\n§|>§|&[^;]+;[ ]*§|Parágrafo único', string[inicio:]))
    r.append(re.search('[\n\t >][a-h]\)', string[inicio:]))
    
    for i in range(5):
        if i == 0:
            menor = r[0]
            if r[0] is None:
                pos = len(string)
                continue
            pos = string.find(r[0].group(), inicio)
        else:
            if r[i] is None:
                pos = len(string)
                continue
            if (string.find(r[i].group(), inicio)) < pos:
                menor = r[i]
                pos = string.find(r[i].group(), inicio)
    
    if menor is None:
        return []
    
    if menor is r[0]:
        return [r[0].group(), pos]
    
    if menor is r[1]:
        return ['SubArtigo', pos]
    
    if menor is r[2]:
        return ['Inciso', pos]
    
    if menor is r[3]:
        return ['Parágrafo', pos]
    
    if menor is r[4]:
        return ['Alinea', pos]


def get_text(string, inicio=0):
    final = string.find('</p>', inicio)
    ignore = re.findall('&[^;]+;|<[^>]*>|\n|\t', string[inicio:final])
    t = ''
    
    ant = inicio
    for i in range(len(ignore)):
        prox = string.find(ignore[i], ant, final)
        t += string[ant:prox]
            
        ant = prox + len(ignore[i])
    
    return t
