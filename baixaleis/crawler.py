import urllib2
from BeautifulSoup import BeautifulSoup as BS

#page = urllib2.urlopen("http://www.planalto.gov.br/ccivil_03/constituicao/constitui%C3%A7ao.htm")

page = open('teste.html', 'r')
soup = BS(page)

soup.findAll('p')

