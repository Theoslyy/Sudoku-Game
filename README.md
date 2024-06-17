This is a Sudoku game project on Python utilizing pygame. It contains an additional Sudoku solver inside. 
The game contains a function that randomly generates a board for each new game. 
The code is mostly commented and below we have an explanation of the part of the code that generates random boards.

The following explanation was made by Gu-Ramos
# Algoritmo de geração do tabuleiro
```python
base = 3
side = base*base

# randomize rows, columns and numbers (of valid base pattern)
from random import sample
def shuffle(s): return sample(s,len(s))
rBase = range(base)
nums = shuffle(range(1,side+1))

rows = [ g*base + r for g in shuffle(rBase) for r in shuffle(rBase) ]
cols = [ g*base + c for g in shuffle(rBase) for c in shuffle(rBase) ]

# pattern for a baseline valid solution
def pattern(r,c): return (base*(r%base)+r//base+c)%side

# produce board using randomized baseline pattern
board = [ [nums[pattern(r,c)] for c in cols] for r in rows ]
```

Ele começa definindo a base e o tamanho do lado do tabuleiro.\
**(A gente vai assumir base 3 e lado 9, e pra todo propósito prático, a gente pode entender um `range` como uma lista.)**


A função `shuffle` só retorna uma versão embaralhada de uma lista qualquer

A variável `rBase` é um range `[0, 1, 2]`

A variável `nums` é uma lista com os números de 1 a 9 `[1, 2, 3, 4, 5, 6, 7, 8, 9]`\
...só que embaralhada!\
A importância dela ser embaralhada é explicada mais tarde, junto com a função `pattern`



# `rows` & `cols`
```python
rows = [ g*base + r for g in shuffle(rBase) for r in shuffle(rBase) ]
cols = [ g*base + c for g in shuffle(rBase) for c in shuffle(rBase) ]
```

Vamos dissecar o que essas duas linhas fazem.\
As duas fazem a mesma coisa: geram uma lista com números de 0 a 8, agrupados em trios `(0,1,2) (3,4,5) (6,7,8)`\
Na lista cada um desses trios é embaralhado, e a ordem dos trios na lista também é embaralhada.

Expandindo uma das linhas temos:
```python
rows = []
S1 = shuffle(rBase) # embaralha uma lista [0, 1, 2]

for g in S1:
	S2 = shuffle(rBase) # embaralha outra lista [0, 1, 2]
	for r in S2:
		rows.append(g*base + r)
```

Vamos analisar o caso base onde `S1`  e `S2` são a lista `[0, 1, 2]`:\
`S1 = [0, 1, 2]`\
`S2 = [0, 1, 2]`

Pegamos o primeiro elemento `g` de `S1` e multiplicamos por **3** (a base)\
(aqui vamos chamar esse produto de `x`)\
Pra cada elemento `r` de `S2` adicionamos na lista `rows` a soma de `x + r`:
```python
x = 0              # g=0,        0*3 = <0>
rows.append( 0 )   # x=0, r=0,   0+0 = <0>
rows.append( 1 )   # x=0, r=1,   0+1 = <1>
rows.append( 2 )   # x=0, r=2,   0+2 = <2>
```

Perceba o que acontece quando vamos para os próximos elementos `g` de `S1`:
```python
x = 3              # g=1,        1*3 = <3>
rows.append( 3 )   # x=3, r=0,   3+0 = <3>
rows.append( 4 )   # x=3, r=1,   3+1 = <4>
rows.append( 5 )   # x=3, r=2,   3+2 = <5>

x = 6              # g=2,        2*3 = <6>
rows.append( 6 )   # x=6, r=0,   6+0 = <6>
rows.append( 7 )   # x=6, r=1,   6+1 = <7>
rows.append( 8 )   # x=6, r=2,   6+2 = <8>
```

Podemos interpretar isso como a combinação entre os elementos de `S1` e `S2`:
- `S1` controla cada um dos grupos `(0,1,2) (3,4,5) (6,7,8)`
- `S2` controla os números de cada grupo controlado por `S1`

Assim, quando embaralhamos `S1`, embaralhamos os trios de listas (ou colunas) do tabuleiro.\
E quando embaralhamos `S2`, embaralhamos os números dentro de cada trio.

# Função `pattern`
É essa a parte mais complicada.
```python
def pattern(r, c): return ( base*(r%base) + r//base + c ) % side
nums = shuffle(range(1,side+1))

board = [ [nums[pattern(r,c)] for c in cols] for r in rows ]
```

À primeira vista, o que se pode inferir é que, é gerado uma lista contendo cada linha do tabuleiro, onde cada número dessa linha é obtido por uma função `pattern`, que retornará o índice de um número `x` (da lista `nums`) para cada elemento `r` e `c` das listas `rows` e `cols`

...complicado!\
Para simplificar as coisas, vamos primeiro assumir `nums` como simplesmente a lista não-embaralhada `[0, 1, 2, 3, 4, 5, 6, 7, 8]`

Também vamos substituir `base` por `3`, e `side` por `9`:\
`( 3*(r%3) + r//3 + c ) % 9`

Vamos dissecar a função `pattern`.\
Essa função vem em 3 partes:
1. `3 * (r%3)` (3 vezes o módulo da divisão de r por 3)
2. `r//3` (divisão inteira de r por 3)
3. `(<1> + <2> + c) % 9` (soma da pt,1 com a pt.2, com c, módulo 9.)

Agora, vamos deixar isso mais legível:
```python
def pattern(r, c):
	a = 3*(r%3)
	b = r//3
	return (a + b + c) % 9
nums = [1, 2, 3, 4, 5, 6, 7, 8, 9]

rows = [0, 1, 2, 3, 4, 5, 6, 7, 8]
cols = [0, 1, 2, 3, 4, 5, 6, 7, 8]

board = [] # inicia o tabuleiro
for r in rows:
	linha = []
	board.append(linha) # adiciona a linha no tabuleiro
	for c in cols:
		p = pattern(r, c)
		linha.append( nums[p] )
```

Vamos ver o que acontece nesse loop aninhado para cada elemento `r, c`
Lembre-se:
- `a = 3*(r%3)`
- `b = r//3`
- `p = (a + b + c) % 9`

Variáveis:

- `rows = [0,1,2,3,4,5,6,7,8]`
- `cols = [0,1,2,3,4,5,6,7,8]`
- `nums = [1,2,3,4,5,6,7,8,9]`

Cada iteração de `rows` (número `r`) gera uma linha.\
As tabelas abaixo mostram cada iteração de `cols` (número `c`) para cada `r`\
Vamos analisar as primeiras 3 iterações de `r` (`rows`) (criação das 3 primeiras linhas)
![Tabela 1](https://i.imgur.com/hbCbb2D.png)

Certo! podemos tirar coisas interessantes daqui:
- A parte `a` da função pattern controla de qual trio da lista `nums` tiraremos o número aletório
- `c` é como um "offset" dentro da lista `nums` que varia para cada coluna. Já que a lista `cols` não possui números repetidos, o offset será diferente para cada coluna, fazendo assim com que não tenhamos repetições.
- O "módulo 9" faz com que essa escolha de `p`  aja como numa lista rotativa. (Isto é, o índice 9 é o mesmo que o índice 0, o índice 10 é o índice 1, e assim por diante. É o módulo da divisão por 9.)

Vamos ver o que acontece quando geramos as próximas 3 linhas:
![Tabela 2](https://i.imgur.com/IdyZnZV.png)

Ahá! Agora sabemos o que a parte `b` faz!
- Se `a` diz de qual trio deveremos tirar o número aleatório, `b` diz qual elemento desse trio será o número aleatório.
- Claro, ainda é aplicado o offset `c` para cada coluna da linha, etc.

Então o resumo da ópera é:
- `a ( 3*(r%3) )`: escolhe de qual trio de `nums` sairá o número aleatório
- `b ( r//3 )`: escolhe qual elemento desse trio será o número aleatório
- `c`: um offset que muda a cada "passo" ou "iteração" de `c`, fazendo com que para cada coluna da linha seja escolhido um número diferente dessa lista `nums`

Para cada 3 iterações de r teremos o mesmo `b`, e 3 `a`'s diferentes.
- `a`: o módulo por 3 varia para cada 3 números e dá `0`, `1`, ou `2`. E como o shuffle de `rows` é feito por trios, cada trio terá 3 "mod3" diferentes (3 `a`'s diferentes.) Cada `a` decide de qual trio sairá o número aleatório, e é justamente porque cada trio tem tamanho 3 (duh) que nós multiplicamos `r%3` por `3`: pra obter o índice certo na lista `nums`.
- `b`: a divisão inteira só vai dar um número diferente "a cada 3 números", e como o shuffle é feito por trios, cada trio de linhas terá sempre o mesmo resultado na divisão inteira por 3.

E cada coluna terá um offset `c` diferente, evitando assim repetições nas linhas.\
(Você pode pensar como: `c` evita repetições nas linhas, `a` evita repetições nos quadrados 3x3, e `b` evita repetições nas colunas!)

Tabuleiro "base" completo:
```
[1,2,3, 4,5,6, 7,8,9]
[4,5,6, 7,8,9, 1,2,3]
[7,8,9, 1,2,3, 4,5,6]
[2,3,4, 5,6,7, 8,9,1]
[5,6,7, 8,9,1, 2,3,4]
[8,9,1, 2,3,4, 5,6,7]
[3,4,5, 6,7,8, 9,1,2]
[6,7,8, 9,1,2, 3,4,5]
[9,1,2, 3,4,5, 6,7,8]
```

Finalmente, se você gerar um tabuleiro com `rows` e `cols` embaralhados, mas o mesmo set de `nums`, você vai perceber que sempre haverão trios de números "sequenciais" em cada lista: (3,2,1), (5,7,6), (8,9,1), etc...

Por isso que nós devemos fazer com que a lista `nums` seja uma lista de números aleatórios entre `1` e `9`, e não apenas uma lista não-embaralhada `[1,2,3,4,5,6,7,8,9]`. É isso que evita esses trios "sequenciais."

:3
