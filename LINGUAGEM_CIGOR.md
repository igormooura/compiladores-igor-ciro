# Documentacao da Linguagem CIgor

## Introducao

A linguagem CIgor e uma linguagem de programacao imperativa de proposito geral, desenvolvida para fins educacionais em um compilador. Ela utiliza uma sintaxe simbolica e abreviada, permitindo expressoes concisas mantendo clareza semantica.

## Tipos de Dados

A linguagem CIgor suporta cinco tipos de dados primitivos:

| Palavra-chave | Tipo          | Descricao                              |
|---------------|---------------|----------------------------------------|
| `In`          | Inteiro       | Numeros inteiros (sem ponto decimal)   |
| `Rac`         | Racional      | Numeros com ponto flutuante            |
| `Ch`          | Caractere     | Um unico caractere                     |
| `Bol`         | Booleano      | Valores verdadeiro (:D) ou falso (:C)  |
| `Txt`         | Texto         | Sequencia de caracteres entre aspas    |

### Exemplo de Declaracao

```
In x;
Rac valor;
Ch letra;
Bol condicao;
Txt mensagem;
```

## Literais

### Literais Booleanos

- `verdadeiro` representado como `:D` (emoticon feliz)
- `falso` representado como `:C` (emoticon triste)

### Literais de Texto

Texto e delimitado por aspas duplas: `"conteudo do texto"`

### Literais de Caractere

Caracteres sao delimitados por aspas simples: `'a'`

### Literais Numericos

- Inteiros: `42`, `0`, `-15`
- Racionais: `3.14`, `2.5`, `-0.5`

## Operadores

### Operadores Aritmeticos

| Operador | Significado | Exemplo |
|----------|-------------|---------|
| `+`      | Adicao      | `a + b` |
| `-`      | Subtracao   | `a - b` |
| `*`      | Multiplicacao | `a * b` |
| `/`      | Divisao     | `a / b` |
| `%`      | Resto (modulo) | `a % b` |

### Operadores Relacionais

| Operador | Significado        | Exemplo  |
|----------|--------------------|----------|
| `?>`     | Maior que          | `a ?> b` |
| `?<`     | Menor que          | `a ?< b` |
| `?>=`    | Maior ou igual     | `a ?>= b` |
| `?<=`    | Menor ou igual     | `a ?<= b` |
| `?=`     | Igual a            | `a ?= b` |
| `?!=`    | Nao igual a        | `a ?!= b` |

### Operadores Logicos

| Operador | Significado | Exemplo |
|----------|-------------|---------|
| `?e`     | Conjuncao (E)    | `a ?e b` |
| `?ou`    | Disjuncao (OU)   | `a ?ou b` |
| `?not`   | Negacao (NAO)    | `?not a` |

### Operador de Atribuicao

| Operador | Significado | Exemplo |
|----------|-------------|---------|
| `=>`     | Atribuicao  | `x => 5` |

## Estruturas de Controle

### Estrutura Condicional - Se/Senao

```
?? (condicao) {
    comandos se verdadeiro;
}
!! {
    comandos se falso;
}
```

Exemplo:
```
In idade;
idade => 18;

?? (idade ?>= 18) {
    Txt msg => "maioridade";
}
!! {
    Txt msg => "menoridade";
}
```

### Laco Enquanto

```
Enq (condicao) {
    comandos;
}
```

Exemplo:
```
In i => 0;

Enq (i ?< 10) {
    i => i + 1;
}
```

### Laco Faca-Enquanto

A construcao `!->` inicia um bloco que se executa pelo menos uma vez antes de verificar a condicao:

```
!-> {
    comandos;
} Enq (condicao);
```

Exemplo:
```
In x => 10;

!-> {
    x => x - 1;
} Enq (x ?> 5);
```

## Funcoes

### Declaracao de Funcao

```
CRIAR tipo_retorno nome(tipo param1, tipo param2) {
    comandos;
    VOLTA valor_retorno;
}
```

Exemplo:
```
CRIAR In soma(In a, In b) {
    VOLTA a + b;
}
```

### Chamada de Funcao

```
In resultado => soma(5, 3);
```

## Vetores

Vetores sao declarados indicando o tamanho entre colchetes:

```
In arr[4];
arr[0] => 10;
arr[1] => 20;
```

O acesso a elemento segue a notacao padrao: `arr[indice]`

## Delimitadores

| Delimitador | Descricao |
|-------------|-----------|
| `(`         | Abre parenteses (expressoes, parametros) |
| `)`         | Fecha parenteses |
| `{`         | Abre bloco de comandos |
| `}`         | Fecha bloco de comandos |
| `[`         | Abre indice de vetor |
| `]`         | Fecha indice de vetor |
| `,`         | Separador de parametros/elementos |
| `.`         | Finalizador de comando (ponto e virgula) |

## Comentarios

Comentarios em CIgor iniciam com `:3` e se estendem ate o final da linha:

```
:3 Isto e um comentario
In x => 5; :3 Comentario no final da linha
```

## Identificadores

Identificadores devem:
- Comecarem com letra (maiuscula ou minuscula) ou sublinhado
- Conter apenas letras, digitos e sublinados
- Nao podem ser palavras-chave reservadas

Exemplos validos: `x`, `_valor`, `contador2`, `ProcessarDados`

## Exemplo Completo

```
In arr[4];
In x;
In y;
Bol condicao;

arr[0] => 1;
arr[1] => 2;
arr[2] => 3;
arr[3] => 4;

CRIAR In somar(In a1, In b1) {
    VOLTA a1 + b1;
}

x => somar(arr[0], arr[1]);

?? (x ?>= 3) {
    x => x + 1;
}
!! {
    x => x - 1;
}

Enq (x ?< 10) {
    x => x + 1;
}

!-> {
    x => x - 1;
} Enq (x ?> 5);

?? (arr[2] ?!= arr[3]) {
    y => y + 2;
}
!! {
    y => y + 0;
}

condicao => (x ?= 6) ?e :D;
```

## Resumo de Sintaxe

| Conceito | Sintaxe |
|----------|---------|
| Tipo inteiro | `In` |
| Tipo racional | `Rac` |
| Tipo caractere | `Ch` |
| Tipo booleano | `Bol` |
| Tipo texto | `Txt` |
| Condicional se | `??` |
| Condicional senao | `!!` |
| Laco enquanto | `Enq` |
| Laco faca-enquanto | `!->` ... `Enq` |
| Criacao de funcao | `CRIAR` |
| Retorno de funcao | `VOLTA` |
| Verdadeiro | `:D` |
| Falso | `:C` |
| Atribuicao | `=>` |
| Maior que | `?>` |
| Menor que | `?<` |
| Maior ou igual | `?>=` |
| Menor ou igual | `?<=` |
| Igual | `?=` |
| Nao igual | `?!=` |
| Conjuncao logica | `?e` |
| Disjuncao logica | `?ou` |
| Negacao logica | `?not` |
| Comentario | `:3` |

## Gramática Formal (EBNF)

Abaixo está a especificação formal da sintaxe de CIgor em notação EBNF:

```ebnf
Programa       ::= Comando*

Comando        ::= Declaracao
                 | Funcao
                 | Retorne
                 | Atribuicao
                 | Se
                 | Enquanto
                 | DoEnquanto

Declaracao     ::= Tipo ID ( "[" NUMERO "]" )? "."

Atribuicao     ::= Destino "=>" ExpressaoLogica "."
Destino        ::= ID ( "[" ExpressaoLogica "]" )?

Se             ::= "??" "(" ExpressaoLogica ")" Bloco ( "!!" Bloco )?

Enquanto       ::= "Enq" "(" ExpressaoLogica ")" Bloco

DoEnquanto     ::= "!->" Bloco "Enq" "(" ExpressaoLogica ")" "."

Funcao         ::= "CRIAR" Tipo ID "(" Parametros? ")" Bloco
Parametros     ::= Parametro ( "," Parametro )*
Parametro      ::= Tipo ID

Retorne        ::= "VOLTA" ExpressaoLogica "."

Bloco          ::= "{" Comando* "}"

ExpressaoLogica ::= ExpressaoRelacional ( OperadorLogico ExpressaoRelacional )*
OperadorLogico  ::= "?e" | "?ou"

ExpressaoRelacional ::= Expressao ( OperadorRelacional Expressao )?
OperadorRelacional  ::= "?>" | "?<" | "?>=" | "?<=" | "?=" | "?!="

Expressao      ::= Termo ( ( "+" | "-" ) Termo )*

Termo          ::= Fator ( ( "*" | "/" | "%" ) Fator )*

Fator          ::= NUMERO
                 | STRING_LITERAL
                 | CARACTERE_LITERAL
                 | ":D"
                 | ":C"
                 | "?not" Fator
                 | ID "(" Argumentos? ")"
                 | ID "[" ExpressaoLogica "]"
                 | ID
                 | "(" ExpressaoLogica ")"

Argumentos     ::= ExpressaoLogica ( "," ExpressaoLogica )*

Tipo           ::= "In" | "Rac" | "Ch" | "Bol" | "Txt"
```

