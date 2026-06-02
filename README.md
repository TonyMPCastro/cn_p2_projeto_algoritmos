# Projeto de Algoritmos Numericos

Este projeto tem como objetivo traduzir formulas matematicas em algoritmos
eficientes usando apenas logica de programacao, lacos de repeticao e estruturas
de dados nativas da linguagem Python.

Ao final da unidade, o pacote computacional devera ser capaz de interpolar dados
e calcular integrais numericas. Nesta primeira versao, o foco esta na
interpolacao polinomial pelos metodos de Lagrange, Newton e Gregory-Newton.

## Objetivos

- Construir algoritmos numericos do zero.
- Evitar bibliotecas externas para reforcar a logica de programacao.
- Organizar o codigo em modulos simples e reutilizaveis.
- Criar exercicios e testes para validar os resultados.

## Estrutura de Pastas

```text
cn_p2_projeto_algoritmos/
+-- README.md
+-- src/
|   +-- __init__.py
|   +-- interpolacao.py
|   +-- plotagem.py
+-- exercicios/
|   +-- 1_interpolacao_.py
|   +-- 2_gregory_newton.py
+-- tests/
    +-- test_interpolacao.py
```

## Interpolacao de Lagrange, Newton e Gregory-Newton

A interpolacao e usada para estimar o valor de uma funcao em um ponto
desconhecido a partir de pontos conhecidos.

O metodo de Lagrange constroi um polinomio que passa por todos os pontos
informados. O metodo de Newton usa diferencas divididas para montar o mesmo
polinomio por coeficientes. O metodo de Gregory-Newton usa diferencas finitas
progressivas e exige pontos igualmente espacados pelo valor de `h`.

As principais funcoes deste projeto sao:

```python
interpolar_lagrange(pontos, x)
interpolar_newton(pontos, x)
interpolar_gregory_newton(pontos, x, h)
```

Elas recebem:

- `pontos`: lista de tuplas no formato `(x, y)`;
- `x`: valor onde se deseja calcular a interpolacao.
- `h`: espacamento constante entre os valores de `x`, usado em
  Gregory-Newton.

Tambem e possivel pedir a contagem de operacoes com
`contar_operacoes=True`. Nesse caso a funcao retorna
`(resultado, operacoes)`, e `operacoes` informa quantas multiplicacoes e
adicoes/subtracoes foram feitas.

Exemplo:

```python
pontos = [(1, 1), (2, 4), (3, 9)]
x = 2.5
resultado, operacoes = interpolar_lagrange(pontos, x, contar_operacoes=True)
```

Saida esperada:

```text
Valor interpolado em x = 2.5: 6.25
Multiplicacoes: 6
Adicoes/subtracoes: 15
```

O exemplo tambem exibe um grafico ASCII no terminal. A curva interpolada aparece
com `*` e os pontos conhecidos aparecem com `o`.

## Exercicio do Drone

O arquivo `exercicios/1_interpolacao_.py` resolve o problema da telemetria do
drone usando Lagrange, Newton e Gregory-Newton.

```python
pontos = [
    (1.0, 1.2),
    (2.0, 1.9),
    (3.0, 3.2),
    (4.0, 5.5),
    (5.0, 8.2),
]
x = 3.5
```

Resultado esperado:

```text
Altitude por Lagrange: 4.2391 metros
Multiplicacoes: 20
Adicoes/subtracoes: 45
Altitude por Newton: 4.2391 metros
Multiplicacoes: 8
Adicoes/subtracoes: 28
Altitude por Gregory-Newton: 4.2391 metros
Multiplicacoes: 8
Adicoes/subtracoes: 19
```

## Exercicio do Servidor

O arquivo `exercicios/2_gregory_newton.py` resolve o problema do sistema de
resfriamento de um servidor usando Gregory-Newton.

```python
pontos = [
    (10, 45.0),
    (20, 52.0),
    (30, 60.0),
    (40, 71.0),
]
x = 25
h = 10
```

Resultado esperado:

```text
Temperatura por Gregory-Newton: 55.75 C
Multiplicacoes: 6
Adicoes/subtracoes: 13
```

## Como Executar

Execute o exercicio do drone:

```powershell
python exercicios/1_interpolacao_.py
```

Execute o exercicio do servidor:

```powershell
python exercicios/2_gregory_newton.py
```

Execute os testes:

```powershell
python -m unittest discover tests
```

## Proximos Passos

- Adicionar outros metodos de interpolacao.
- Implementar integracao numerica.
- Criar mais exemplos de uso.
- Expandir os testes automatizados.
