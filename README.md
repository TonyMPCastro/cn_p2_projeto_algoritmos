# Projeto de Algoritmos Numericos

Este projeto tem como objetivo traduzir formulas matematicas em algoritmos
eficientes usando apenas logica de programacao, lacos de repeticao e estruturas
de dados nativas da linguagem Python.

Ao final da unidade, o pacote computacional devera ser capaz de interpolar dados
e calcular integrais numericas. Nesta primeira versao, o foco esta na
interpolacao polinomial pelos metodos de Lagrange e Newton.

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
+-- tests/
    +-- test_interpolacao.py
```

## Interpolacao de Lagrange e Newton

A interpolacao e usada para estimar o valor de uma funcao em um ponto
desconhecido a partir de pontos conhecidos.

O metodo de Lagrange constroi um polinomio que passa por todos os pontos
informados. O metodo de Newton usa diferencas divididas para montar o mesmo
polinomio por coeficientes.

As principais funcoes deste projeto sao:

```python
interpolar_lagrange(pontos, x)
interpolar_newton(pontos, x)
```

Elas recebem:

- `pontos`: lista de tuplas no formato `(x, y)`;
- `x`: valor onde se deseja calcular a interpolacao.

Exemplo:

```python
pontos = [(1, 1), (2, 4), (3, 9)]
x = 2.5
resultado = interpolar_lagrange(pontos, x)
```

Saida esperada:

```text
Valor interpolado em x = 2.5: 6.25
```

O exemplo tambem exibe um grafico ASCII no terminal. A curva interpolada aparece
com `*` e os pontos conhecidos aparecem com `o`.

## Exercicio do Drone

O arquivo `exercicios/1_interpolacao_.py` resolve o problema da telemetria do
drone usando Lagrange e Newton.

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
Altitude por Newton: 4.2391 metros
```

## Como Executar

Execute o exercicio do drone:

```powershell
python exercicios/1_interpolacao_.py
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
