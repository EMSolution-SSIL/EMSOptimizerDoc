---
sidebar_position: 3
---

# rastrigin
The Rastrigin single-objective optimization benchmark function\[11\].

## Overview
The Rastrigin function is defined as follows. It is known as a multimodal function whose optimal solution is $\boldsymbol{x}=\boldsymbol{0}$. It is one of the problems considered relatively difficult to optimize with CMA-ES\[12\].
```math
f(\boldsymbol{x}) = 10n + \sum_{i=1}^{n} [x_{i}^{2}-10 \cos (2 \pi x_i)] \\
-5.12 \leq x_i \leq 5.12
```

## Configurable keyword arguments
- `dim: int` ... Number of dimensions $n$ in the optimization problem.
