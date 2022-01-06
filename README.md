# pybench

Pybench é uma estrutura para realizar benchmark de funções da maneira mais simples possível.

## Instalação

Para a instalação é possível usar a ferramenta pip com o seguinte comando:

    pip install git+https://github.com/emanuel-alves/pybench.git

## Exemplo de uso

Exemplos de implementações podem ser encontrados na pasta /example, entretanto pode ser visto uma forma de implementação generica abaixo:

```python
from pybench import Benchmark

def f1(arg1, arg2, ...):
    ...

def f2(arg1, arg2, ...):
    ...

...

bench = Benchmark(functions=[f1, f2, ...],
                  args=[arg1, arg2, ...],
                  numTests=1)

print(bench)

```
    