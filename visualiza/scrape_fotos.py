# -*- coding:utf-8 -*-
"""
Modulo para baixar as fotos dos ministros do supremo
"""
import mechanize
import urllib2

#root = lxml.html.fromstring(html)

def download_photo(url, texto):
    """
    Downloads the images and save them to files named after the ministers
    """
    raw_im = urllib2.urlopen(url).read()
    print texto
    with open('imagens/'+texto+'.jpg', 'wb') as f:
        f.write(raw_im)

br = mechanize.Browser()
br.open("http://www.stf.jus.br/portal/ministro/ministro.asp?periodo=stf&tipo=antiguidade")
i = 0
link = br.find_link(url_regex=r'verMinistro.asp', nr=i)
while 1:
    br.follow_link(link)
    il = br.find_link(url_regex='imagem.asp')
    print i, il.url
    url = "http://www.stf.jus.br/portal"+ il.url.strip('..')
    nome = il.text
    download_photo(url, nome.decode('latin1').split('[')[0])
    br.back()
    try:
        link = br.find_link(url_regex=r'verMinistro.asp', nr=i)
    except LinkNotFoundError:
        break
    i += 1



