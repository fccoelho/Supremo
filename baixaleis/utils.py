# -*- coding:utf-8 -*-

import re


def get_next_tag(string):
    r = re.search('>LIVRO|>TÍTULO|>CAPÍTULO|>SEÇÃO|>Subseção|Art.')
    if r != None:
        return [r.group(), string.find(r.group())]
    return []
    
def get_text:
    pass
