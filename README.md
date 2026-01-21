# TrabalhoCG1
ainda iremos descobrir! descubra!

## Erros de POO (Programação Orientada a Objetos) detectados

Abaixo estão problemas de modelagem/POO encontrados no código, com a indicação de onde ocorrem e o que representam.

1) Uso de estado global e acoplamento implícito entre módulos
- Onde:
  - SerVivo.py: linhas 4–7 (largura, altura, passo, energia_padrao, energia_reproducao)
  - Planta.py: linha 11 (usa `passo` importado indiretamente)
  - Mosquito.py: linha 11 (usa `passo` importado indiretamente)
  - Main.py: linha 12 (duplica largura/altura) e linhas 5–9 (imports com `*`)
- O que é o problema:
  - Variáveis globais de configuração espalhadas dificultam encapsulamento e manutenção (violam princípio de responsabilidade única e aumentam acoplamento).
  - O uso de `from ... import *` oculta dependências e cria acoplamento implícito: `Planta` e `Mosquito` dependem de `passo` definido em SerVivo.py, sem torná‑lo explícito.
  - Duplicação de `largura/altura` em SerVivo.py e Main.py pode levar a inconsistências.
- Sugestão:
  - Centralizar configuração em um módulo/objeto de configuração ou em atributos de classe.
  - Evitar `import *`; importar nomes explícitos ou passar dependências por parâmetro.

2) Violação da Lei de Demeter / responsabilidade inadequada do objeto
- Onde:
  - SerVivo.py: linhas 29–34 dentro de `SerVivo.mover`
- O que é o problema:
  - `SerVivo` remove a si mesmo diretamente das listas globais `plantas`/`animais`. O gerenciamento do ciclo de vida dos objetos deveria ser responsabilidade do “mundo”/motor da simulação, não do agente individual.
- Sugestão:
  - Delegar remoções ao controlador/ambiente (ex.: retorno de um evento/estado) em vez de manipular coleções externas.

3) Baixa coesão e acoplamento entre classes dentro de `mover`
- Onde:
  - SerVivo.py: linhas 15–24 e regra geral de `mover`
- O que é o problema:
  - O método `mover` do tipo base conhece a estrutura completa do mundo (`plantas + animais`) e aplica regras de colisão. Isso mistura responsabilidades de “motor” da simulação com a de um agente, criando acoplamento entre `SerVivo` e todas as demais entidades.
- Sugestão:
  - Extrair a lógica de vizinhança/colisão para um objeto Ambiente/Mundo, ou fornecer uma interface clara que o agente consulte sem conhecer detalhes das coleções.

4) Método com retorno de tipos mistos/sentinelas mágicos
- Onde:
  - SerVivo.py: linhas 63–74 em `gastarEnergia`
- O que é o problema:
  - O método retorna `-1`, `0` ou um novo objeto. Esse contrato polimórfico é frágil e obriga o chamador a lidar com códigos mágicos, o que reduz legibilidade e robustez.
- Sugestão:
  - Retornar um objeto de resultado (ex.: enum/estado + payload) ou lançar eventos; separar claramente “tick de energia” e “reprodução”.

5) Classe base define comportamentos que não se aplicam a todas as subclasses
- Onde:
  - SerVivo.py: `mover` existe para todo `SerVivo`
  - Planta.py: `Planta` herda `SerVivo` (linha 7), mas plantas não se movem; ainda assim a classe base fornece `mover` para todas as subclasses.
- O que é o problema:
  - O modelo da hierarquia dá a entender que todo ser vivo se move, o que não é verdade para plantas. Isso é um sinal de hierarquia inadequada.
- Sugestão:
  - Tornar `SerVivo` mais abstrata (apenas estado comum) e mover `mover` para uma sub-hierarquia de seres móveis (ex.: `SerMovel`). Ou sobrescrever `mover` em `Planta` como no‑op.

6) Ausência de abstração formal para comportamentos obrigatórios
- Onde:
  - Animal.py: linhas 7–9 (`Animal.predar` é um método concreto que não faz nada)
- O que é o problema:
  - `predar` parece ser obrigatório para animais, mas a classe base não força implementação. Subclasses podem “esquecer” de sobrescrever e o erro passa despercebido.
- Sugestão:
  - Tornar `Animal` uma classe abstrata e `predar` um `@abstractmethod` (ou lançar `NotImplementedError`).

7) Acoplamento de desenho e domínio através de nomes genéricos e funções globais
- Onde:
  - Graficos.py: funções livres `setMosquito` são usadas para desenhar qualquer entidade (Main.py linhas 40 e 52)
- O que é o problema:
  - O nome específico (`setMosquito`) para desenhar diferentes tipos indica acoplamento conceitual e reduz clareza.
- Sugestão:
  - Renomear para algo neutro (ex.: `desenhar_quadrado`) ou introduzir um Renderer desacoplado do domínio.

8) Importações com wildcard e poluição de namespace
- Onde:
  - Main.py: linhas 5–9
  - Animal.py, Planta.py, Mosquito.py: linha 4
- O que é o problema:
  - `from ... import *` dificulta rastrear de onde vêm nomes e pode causar colisões. Também mascara dependências (ex.: `passo`).
- Sugestão:
  - Importar apenas o que é necessário: `from SerVivo import SerVivo, passo` (idealmente, evitar a dependência a `passo`).

9) Encapsulamento fraco de estado
- Onde:
  - SerVivo.py: atributos `x`, `y`, `energia` são públicos e manipulados diretamente em vários módulos
- O que é o problema:
  - Sem getters/setters ou propriedades, invariantes (ex.: limites de tela, energia mínima/máxima) podem ser quebrados inadvertidamente.
- Sugestão:
  - Usar propriedades para validar alterações ou centralizar regras no Ambiente.

Observações adicionais (não estritamente POO, mas relevantes):
- Remover itens das listas enquanto se itera pode causar erros sutis. Ex.: Main.py linhas 39–47 removem plantas durante a iteração. O padrão mais seguro é iterar sobre uma cópia ou acumular remoções para aplicar depois.
- Em `Planta.fotossintese` (linhas 9–13) a contagem de vizinhos inclui a própria planta (distância zero), o que pode ou não ser desejado.
- Em `SerVivo.mover` a lógica de direção/collision checking é confusa (ex.: mover para 'N' incrementa `y`, que em coordenadas de tela costuma ser sul). Não é POO, mas pode indicar bug lógico.
