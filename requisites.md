# Requisitos da Linguagem de Programação

### Compiladores

### Ciência da Computação

### Prof. Daniel Saad Nogueira Nunes


## Introdução

Na disciplina de Compiladores, o objetivo é produzir um tradutor capaz de converter
uma linguagem alto-nível para o assemblySaM.
Essa linguagem deve possuir alguns requisitos mínimos, listados a seguir.

## Requisitos

Paradigma: Procedural. Os códigos da linguagem projetada devem ser organizados
em funções e procedimentos, comoCouPascal.

Tipos primitivos: A linguagem deve possuir, no mínimo, suporte a tipos inteiros,
ponto-flutuante de precisão simples (IEEE-754) e caracteres.

Variáveis: A linguagem deve possuir suporte a variáveis.

Vetores e Strings (opcional): sequências homogêneas de dados primitivos devem ser
suportadas.

Constantes: constantes numéricas devem ser suportadas.

Atribuição: a atribuição entre posições de memórias deve ser suportada.

Operadores aritméticos: no mínimo, devem ser suportados os operadores de:

- Adição;
- Subtração;
- Multiplicação;
- Divisão;
- Resto.

Operadores relacionais: no mínimo, devem ser suportados os operadores relacionais
de:

- Igualdade;
- Diferença;
- Maior;
- Menor;
- Maior ou igual;
- Menor ou igual;
    1


Operadores lógicos: no mínimo, devem ser suportados os seguintes operadores lógicos:

- Conjunção (E);
- Disjunção (Ou);
- Negação (Não);

Funções (Opcional): funções e procedimentos devem ser suportados na linguagem.

Opcionais:

- Tipo booleano.
- Operadores bit-a-bit.
- Constantes de strings;

Estruturas de decisão: estruturasse, entãoesenãodevem ser suportadas.

Estruturas de repetição: no mínimo uma das estruturas de repetição abaixo deve
ser suportada:

- Repetição com teste no início (While, ou for);
- Repetição com teste no final (Do while);

## Restrições

Não serão permitidos geradores de código para análise léxica ou sintática. Esses
componentes devem ser explicitamente implementados.
O trabalho poderá ser feito individualmente ou em duplas.

## Avaliação

```
Serão avaliados os seguintes itens:
```
- Projeto da gramática;
- Análise léxica;
- Análise sintática;
- Análise semântica;
- Geração de código;
- Testes e documentação.

```
2
```

