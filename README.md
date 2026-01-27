# EcoSim

Simulação 2D de um ecossistema (plantas, presas e predadores) feita em **Python + Pygame**.

A simulação roda em *ticks*. Em cada tick:
- seres vivos gastam energia;
- podem morrer ou se reproduzir;
- animais se movem e podem predar;
- plantas realizam “fotossíntese” para recuperar energia.

---

## Sumário

- [Demonstração / o que você vai ver](#demonstração--o-que-você-vai-ver)
- [Requisitos](#requisitos)
- [Instalação](#instalação)
- [Como executar](#como-executar)
  - [Menu](#menu)
- [Como funciona (alto nível)](#como-funciona-alto-nível)
- [Estrutura do projeto](#estrutura-do-projeto)
- [Regras da simulação (detalhes do modelo)](#regras-da-simulação-detalhes-do-modelo)
  - [Energia, reprodução e morte](#energia-reprodução-e-morte)
  - [Movimento e colisão](#movimento-e-colisão)
  - [Plantas: fotossíntese](#plantas-fotossíntese)
  - [Presas e predadores: predação](#presas-e-predadores-predação)

---

## Demonstração / o que você vai ver

Ao executar, abre uma janela do Pygame com:

- **Menu**, onde são escolhidos os biomas e a quantidade de entidades que existirão quando a simulação começar;
- após clicar no botão "Inicio", o programa abre um **mundo principal**, onde as entidades são desenhadas;
- e uma **mini-viewport** no canto superior esquerdo (um “mapa” mostrando marcadores de plantas e animais).

Comportamentos típicos:
- plantas aumentam energia e se espalham, mas podem morrer se ficarem sem energia;
- presas procuram plantas quando estão com fome;
- predadores caçam presas quando estão com fome;
- reprodução acontece quando a energia ultrapassa um limiar.

---

## Requisitos

- **Python 3.10+** (recomendado)
- **pygame**

---

## Instalação

1) Baixe/clone e entre na pasta do projeto.

2) (Recomendado) crie um ambiente virtual.

3) Instale as dependências.

Exemplo (PowerShell):

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install pygame
```

---

## Como executar

### Menu

O menu é uma UI em Pygame com botões.

```powershell
python .\Menu.py
```

Botões:
- **INICIO**: fecha o menu e chama `Inicializacao.main()`.
- **BIOMA**: alterna o texto *FLORESTA/MAR*.
- **ANIMAIS**: alterna um número (21/35/49).
- **SAIR**: fecha o programa.

No `Inicializacao.py` são definidos:
- tamanho da janela/mundo (`largura`, `altura`)
- tamanho do passo no grid (`escala`)
- população inicial (quantidade de plantas, presas, predadores)

---

## Como funciona (alto nível)

- **Entrada**:
  - `Menu.py` → chama `Inicializacao.main()`
  - ou rodar `Inicializacao.py` direto

- **Loop principal** (`Inicializacao.main()`):
  1. processa eventos (fechar janela);
  2. chama `mundo.tick()` para avançar a simulação;
  3. chama `mundo.desenhar()` para renderizar;
  4. limita o FPS (no código atual: `clock.tick(10)`).

- **Tick do mundo** (`Mundo.tick()`):
  - plantas: gastam energia → podem reproduzir/morrer → fotossíntese
  - animais: gastam energia → podem reproduzir/morrer → animam → movem → predam

---

## Estrutura do projeto

### Início

- `Menu.py`
  - Menu em Pygame (desenhado com rotinas do próprio projeto), com botões.

- `Inicializacao.py`
  - Inicializa Pygame, cria um `Mundo`, popula entidades aleatórias e executa o loop.

### Simulação

- `Mundo.py`
  - Classe `Mundo`: mantém listas de `plantas` e `animais`.
  - `tick()`: avança 1 passo da simulação.
  - `desenhar()`: desenha mundo + mini-viewport.
  - `spawn_filho(pai)`: cria um novo ser do mesmo tipo e tenta deslocá-lo.

- `SerVivo.py`
  - Classe base `SerVivo`: posição, energia, regras de reprodução/morte e movimento.

- `Animal.py`
  - Classe base `Animal(SerVivo)` com gancho `predar()`.

- `Planta.py`
  - `Planta(SerVivo)`: define `fotossintese()` e `desenhar()`.

- `Presa.py`
  - `Presa(Animal)`: implementa `predar()` (come plantas quando está com fome).

- `Predador.py`
  - `Predador(Animal)`: implementa `predar()` (come presas quando está com fome) e animação com “língua”.

- `Energia.py`
  - Define `EnergiaStatus` (`VIVO`, `MORTO`, `REPRODUZINDO`) e a dataclass `StatusEnergia`.

### Gráficos e utilitários

- `Graficos.py`
  - Primitivas e rotinas de desenho (pixel, preenchimento, sprites/figuras “na unha”).
  - Funções usadas por entidades: `setPlanta`, `setMosca`, `setSapo`, etc.

- `Fonte.py`
  - Fonte bitmap e helper `draw_text()` (o menu usa isso).

- `Transformacoes.py`
  - Matrizes e transformações para mapear coordenadas do mundo para a mini-viewport.

---

## Regras da simulação (detalhes do modelo)

### Energia, reprodução e morte

A regra é centralizada em `SerVivo.gastarEnergia()`:

- **Reprodução**: se `energia > energia_reproducao`
  - o ser perde `energia_padrao` e retorna status `REPRODUZINDO`.
  - o `Mundo` cria um filho com `type(pai)(pai.x, pai.y)`.

- **Vivo**: se `energia > 0`
  - perde `custo_energetico` por tick.

- **Morte**: se `energia <= 0`
  - retorna status `MORTO` e o `Mundo` remove o ser da lista.

Observação: para predadores, o `custo_energetico` é menor (`Predador.custo_energetico = 2`) para sobreviver mais tempo sem presas.

### Movimento e colisão

- Movimento é em grade (passo fixo): `SerVivo.escala`.
- A cada tick, o ser tenta mover para uma das direções `N/S/E/W` em ordem aleatória.
- Restrições:
  - não pode sair dos limites do mundo;
  - não pode ocupar uma célula já ocupada por planta/animal.

Se o ser tentar as 4 direções e não conseguir mover, ele é removido do mundo (isso acontece dentro de `SerVivo.mover()`).

### Plantas: fotossíntese

Em `Planta.fotossintese(plantas, animais)`:
- conta plantas vizinhas (distância em *grid* com alcance `2 * escala`);
- se tiver **muitos vizinhos** (>= 4), não ganha energia (interpretação: pouca luz);
- senão, ganha energia:
  - **+20** se houver mais de 5 animais no mundo (interpretação: polinização/fertilização);
  - **+5** caso contrário.

### Presas e predadores: predação

- `Presa.predar()`:
  - se `energia < energia_fome`, procura uma planta adjacente (até 1 passo) e come:
    - remove a planta da lista
    - `energia += 300`

- `Predador.predar()`:
  - se `energia < energia_fome`, procura um animal de outro tipo adjacente (até 1 passo) e come:
    - remove a presa da lista
    - `energia += 120`
    - ativa uma animação de “língua” no sapo (`lingua = 4`).

---

### Mundo / grid (em `Inicializacao.py`)

- `largura, altura, escala = 1000, 800, 20`
- População inicial:
  - Escala em x:2x:4x com opções entre 21 entidades, 35 entidades ou 49 entidades.

### Dinâmica de energia (em `SerVivo.py`)

- `energia_padrao = 300`
- `energia_reproducao = 500`
- `custo_energetico = 7`
- `energia_fome = 230`

Valores específicos:
- `Planta.custo_energetico = 3`
- `Predador.custo_energetico = 2`
- `Predador.energia_fome = 1000`

---