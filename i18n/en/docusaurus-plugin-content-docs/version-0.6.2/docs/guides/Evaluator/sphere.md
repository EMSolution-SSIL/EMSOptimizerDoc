---
sidebar_position: 2
---

# sphere
The Sphere single-objective optimization benchmark function\[11\].

## Overview
The Sphere function is defined as follows. It is known as a unimodal function whose optimal solution is $\boldsymbol{x}=\boldsymbol{0}$.
```math
f(\boldsymbol{x}) = \sum_{i=1}^{n} x_{i}^{2}\\
-5.12 \leq x_i \leq 5.12
```

## Configurable keyword arguments
- `dim: int` ... Number of dimensions $n$ in the optimization problem.
