## Problema de coloração de grafos

Dado um grafo qualquer _G = (V,E)_, vamos determinar a quantidade mínima de cores para se colorir este grafo. Vértices adjacentes não podem possuir a mesma cor.

### Parâmetros

- Conjunto de vértices do grafo: _V_;
- Conjunto de arcos do grafo: _E_.

### Variáveis

- <img src="https://latex.codecogs.com/svg.latex?w_{j} \in \{0,1\}" title="\Large x=\frac{-b\pm\sqrt{b^2-4ac}}{2a}" />  igual a 1 se a cor _j_ foi utilizada;
- <img src="https://latex.codecogs.com/svg.latex?x\*{ij} \in \{0,1\}" title="\Large x=\frac{-b\pm\sqrt{b^2-4ac}}{2a}" />  igual a 1 se o vértice _i_ é colorido com a cor _j_.

### Função objetivo

Minimizar a quantidade de cores:

<img src="https://latex.codecogs.com/svg.latex?\begin{equation}\mbox{minimize} \sum_{i = 0}^{N} w_{j}
\end{equation}" title="\Large x=\frac{-b\pm\sqrt{b^2-4ac}}{2a}" />

### Restrições

- Cada vértice deve ser colorido com exatamente uma cor;
- Vértices adjacentes não devem ser coloridos com cores distintas.

<img src="https://latex.codecogs.com/svg.latex? \begin{equation}
  \sum_{j = 0}^{N} x_{ij} = 1, \mbox{ }\forall i \in V\\
  x_{ij} + x_{kj} \le w_{j}, \mbox{ } \forall (i, k) \in E \mbox{ } \forall j \in N
  \end{equation}" title="\Large x=\frac{-b\pm\sqrt{b^2-4ac}}{2a}" />
