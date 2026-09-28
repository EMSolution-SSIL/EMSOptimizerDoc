---
sidebar_position: 4
---

# zdt1
The ZDT1 multi-objective optimization benchmark function\[9\].

## Overview
The ZDT1 function is defined as follows.
```math
f_1(\boldsymbol{x}) = x_1 \\
f_2(\boldsymbol{x}) = g(\boldsymbol{x}) h(\boldsymbol{x}) \\
g(\boldsymbol{x}) = 1 + 9 \sum_{i=2}^{n} x_i \\
h(\boldsymbol{x}) = 1 - \sqrt{f_1 / g} \\
0 \leq x_i \leq 1
```

## Configurable keyword arguments
- `dim: int` ... Number of dimensions $n$ in the optimization problem.
