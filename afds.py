"""
ATIVIDADE 1 --- Analisador lexico de declaracoes de variaveis

Trabalhe em ordem, de cima para baixo. Rode `python3 testar.py` a cada
mudanca: ele para no primeiro nivel que falha e da uma dica.

Ferramentas:

  afd(estados, transicoes, inicial, finais)
      Monta um AFD completo. Todo par (estado, simbolo) que voce nao
      declarar vai para o estado de erro, e erro rejeita.

  de(conjunto, destino)
      de(DIGITOS, 'n1')  ->  {'0':'n1', '1':'n1', ..., '9':'n1'}

  Conjuntos prontos: LETRAS DIGITOS SUBLIN BRANCOS PONTO BARRA IGUAL
                     PVIRG SIGMA
  Combine com | (uniao) e - (diferenca).   Ex: SIGMA - {'\n'}
"""
from mini_base import (afd, de, LETRAS, DIGITOS, SUBLIN, BRANCOS,
                       PONTO, BARRA, IGUAL, PVIRG, SIGMA)

# ======================================================================
# NIVEL 0 --- ja vem pronto. Leia com atencao: sao os seus modelos.
# ======================================================================

# identificador: letra ou sublinhado, seguido de letra, digito ou sublinhado
afd_id = afd(
    estados=['i0', 'i1'],
    transicoes={
        'i0': de(LETRAS | SUBLIN, 'i1'),
        'i1': de(LETRAS | DIGITOS | SUBLIN, 'i1'),
    },
    inicial='i0',
    finais=['i1'],
)

# espacos: um ou mais
afd_branco = afd(
    estados=['b0', 'b1'],
    transicoes={
        'b0': de(BRANCOS, 'b1'),
        'b1': de(BRANCOS, 'b1'),
    },
    inicial='b0',
    finais=['b1'],
)

# ======================================================================
# NIVEL 1 --- literal inteiro:  um ou mais digitos.   Ex: 0  42  13
# ======================================================================
afd_inteiro = afd(
    estados=['n0', 'n1'],
    transicoes={
        'n0': de(DIGITOS, 'n1'),
        'n1': de(DIGITOS, 'n1'),
    },
    inicial='n0',
    finais=['n1'],
)

# ======================================================================
# NIVEL 2 --- atribuicao e ponto e virgula: um caractere cada.
# ======================================================================
afd_atrib = afd(
    estados=['a0', 'a1'],
    transicoes={
        'a0': de(IGUAL, 'a1'),
    },
    inicial='a0',
    finais=['a1'],
)

afd_pvirg = afd(
    estados=['p0', 'p1'],
    transicoes={
        'p0': de(PVIRG, 'p1'),
    },
    inicial='p0',
    finais=['p1'],
)

# ======================================================================
# NIVEL 3 --- palavras reservadas de tipo
# Nao e automato novo. Va ao dicionario PALAVRAS, no fim do arquivo.
# ======================================================================

# ======================================================================
# NIVEL 4 --- literal real:  digitos, ponto, digitos.   Ex: 7.5  0.0  6.25
#
# ATENCAO: "12." NAO e um real. Ao decidir os estados finais, pergunte-se
# o que acontece se a palavra terminar logo depois do ponto.
# ======================================================================
afd_real = afd(
    estados=['r0', 'r1', 'r2', 'r3'],
    transicoes={
        'r0': de(DIGITOS, 'r1'),
        'r1': {**de(DIGITOS, 'r1'), **de(PONTO, 'r2')},
        'r2': de(DIGITOS, 'r3'),
        'r3': de(DIGITOS, 'r3'),
    },
    inicial='r0',
    finais=['r3'],           # r2 (logo apos o ponto) NAO e final
)

# ======================================================================
# NIVEL 5 --- literais logicos: verdadeiro e falso
# Tambem no dicionario PALAVRAS.
# ======================================================================

# ======================================================================
# NIVEL 6 --- comentario de linha:  // e tudo ate o fim da linha
# Dica: SIGMA - {'\n'} e tudo menos a quebra de linha.
# ======================================================================
afd_comentario = afd(
    estados=['c0', 'c1', 'c2'],
    transicoes={
        'c0': de(BARRA, 'c1'),
        'c1': de(BARRA, 'c2'),
        'c2': de(SIGMA - {'\n'}, 'c2'),
    },
    inicial='c0',
    finais=['c2'],
)

# ======================================================================
# A ORDEM das regras desempata casamentos de MESMO tamanho.
# Para esta atividade a ordem abaixo ja esta correta. Nao mexa ainda.
# ======================================================================
REGRAS = [
    ('COMENTARIO', afd_comentario),
    ('BRANCO',     afd_branco),
    ('REAL',       afd_real),
    ('INTEIRO',    afd_inteiro),
    ('ID',         afd_id),
    ('ATRIB',      afd_atrib),
    ('PVIRG',      afd_pvirg),
]

# ======================================================================
# PALAVRAS reservadas: lexema -> categoria do token
# Uma palavra reservada e um identificador que esta nesta tabela.
# ======================================================================
PALAVRAS = {
    # nivel 3
    'inteiro': 'TIPO',
    'real': 'TIPO',
    'logico': 'TIPO',
    # nivel 5
    'verdadeiro': 'LOGICO',
    'falso': 'LOGICO',
}

DESCARTAR = {'COMENTARIO', 'BRANCO'}
