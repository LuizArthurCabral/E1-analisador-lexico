# E1 — Analisador léxico: relatório

Nome: _______________

## Autômatos

Convenção: `(( ))` = estado final, `ERRO` omitido (todo símbolo não desenhado vai para ele).

### 1. Inteiro — `afd_inteiro` (2 estados)

```
   ──▶ ( n0 ) ──dígito──▶ (( n1 ))
                              ↺ dígito
```

| estado | o que lembra |
|---|---|
| `n0` | ainda não vi nenhum dígito |
| `n1` | já vi pelo menos um dígito (aceita; mais dígitos continuam valendo) |

Dois estados porque só há duas respostas para "já vi um dígito?".

### 2. Atribuição — `afd_atrib` (2 estados)

```
   ──▶ ( a0 ) ──'='──▶ (( a1 ))
```

| estado | o que lembra |
|---|---|
| `a0` | nada consumido ainda |
| `a1` | já li exatamente um `=` (aceita) |

`a1` não tem transição: um segundo `=` vai para ERRO, então `==` vira dois tokens.

### 3. Ponto e vírgula — `afd_pvirg` (2 estados)

```
   ──▶ ( p0 ) ──';'──▶ (( p1 ))
```

| estado | o que lembra |
|---|---|
| `p0` | nada consumido ainda |
| `p1` | já li um `;` (aceita) |

### 4. Real — `afd_real` (4 estados)

```
                 dígito          '.'           dígito
   ──▶ ( r0 ) ─────────▶ ( r1 ) ─────▶ ( r2 ) ─────────▶ (( r3 ))
                          ↺ dígito                          ↺ dígito
```

| estado | o que lembra |
|---|---|
| `r0` | nada consumido ainda |
| `r1` | já vi a parte inteira (um ou mais dígitos), ainda sem ponto |
| `r2` | vi a parte inteira e o ponto, mas ainda nenhum dígito fracionário |
| `r3` | vi dígitos, ponto e pelo menos um dígito depois (aceita) |

Quatro estados porque são quatro situações distintas. **`r2` não é final**: assim `12.`
não é real. O casamento mais longo faz o analisador ler `12` como INTEIRO e
depois reportar erro em `.`.

### 5. Comentário de linha — `afd_comentario` (3 estados)

```
                 '/'            '/'            tudo menos '\n'
   ──▶ ( c0 ) ───────▶ ( c1 ) ───────▶ (( c2 ))
                                          ↺ SIGMA − {'\n'}
```

| estado | o que lembra |
|---|---|
| `c0` | nada consumido ainda |
| `c1` | vi uma `/`; preciso de outra para ser comentário |
| `c2` | estou dentro do comentário (aceita); continua até aparecer `\n` |

`c1` não é final, então uma `/` sozinha dá erro léxico (divisão fica para a atividade 2).
Como `c2` não aceita `\n`, a quebra de linha fica fora do comentário.

### Já prontos (nível 0) e palavras reservadas

- `afd_id` (2 estados) e `afd_branco` (2 estados) vieram prontos.
- Níveis 3 e 5 **não têm autômato novo**: `inteiro`, `real`, `logico` → `TIPO` e
  `verdadeiro`, `falso` → `LOGICO` no dicionário `PALAVRAS`. Uma palavra reservada é um
  ID que consta na tabela; por isso `inteirox` continua sendo ID.

## Contagem de estados

| autômato | estados (sem ERRO) | por quê |
|---|---|---|
| inteiro | 2 | "já vi dígito?" sim/não |
| atrib | 2 | antes / depois do `=` |
| pvirg | 2 | antes / depois do `;` |
| real | 4 | antes, parte inteira, após o ponto, parte fracionária |
| comentário | 3 | antes, uma barra, dentro do comentário |

## O nível que me deu mais trabalho 

O nível 4 (literal real) foi o que exigiu mais cuidado, porque é o único autômato com quatro estados e com uma armadilha na escolha dos estados finais. 
Para entender o problema, testei o erro de propósito: marquei `r2`, o estado logo depois do ponto, como final (`finais=['r2', 'r3']`). O `testar.py` falhou no nível 4 com a entrada `'12.'`. O esperado era erro léxico, mas o obtido foi `[('REAL', '12.')]`. O analisador aceitava `12.` como número real. 
A causa é que, em `r2`, eu já li os dígitos e o ponto, mas ainda não li nenhum dígito depois dele. Um real válido precisa de pelo menos um dígito na parte fracionária, então `r2` não pode ser de aceitação. Só `r3`, que lembra "já vi ao menos um dígito depois do ponto", pode ser final. 
Corrigi voltando para `finais=['r3']`. Com isso, `12.` não casa como REAL e o analisador lê `12` como INTEIRO, depois reporta erro no `.`. O nível 4 passou e os seguintes continuaram passando. Aprendi que o que define se um estado é final é o que ele lembra, não a posição dele no desenho.
