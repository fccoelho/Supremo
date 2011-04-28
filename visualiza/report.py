# -*- coding:utf-8 -*-
"""
Gera um documento Latex com o resultado de varias analises
"""
import os

esqueleto = r"""
\documentclass[a4paper,10pt]{report}
\usepackage[utf8x]{inputenc}
\title{%s}
\author{Flávio Codeço Coelho}

\begin{document}
\maketitle

\begin{abstract}
\include{resumo}
\end{abstract}
\include{corpo}
\end{document}     
"""

def compila_relatorio():
    """
    Compila relatorio em latex para gerar PDF
    """
    with open('relatorio.tex', 'w') as f:
        f.write(esqueleto)
    os.system('pdflatex -interaction=nonstopmode relatorio.tex')
