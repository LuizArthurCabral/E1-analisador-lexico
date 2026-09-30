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

> **Preencha com a sua experiência real** — esta seção vale 10% e é sobre o que
> aconteceu com você. Responda: qual nível travou, o que estava errado na primeira
> tentativa e como você percebeu (qual saída do `testar.py` mostrou o problema).
>
> Erros comuns, se algum deles for o seu: marcar `r2` como final (`12.` passa);
> esquecer o `de(PONTO, ...)` em `r1`; colocar laço em `a0` (`==` vira um token só);
> usar `SIGMA` sem tirar `'\n'` no comentário (engole as linhas seguintes).
