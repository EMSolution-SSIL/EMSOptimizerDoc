---
sidebar_position: 2
---

# ls_r
A simple LevelSetFunction implementation that assigns levels according to the radius.

## Overview
For example, when the configuration `num_level` is `3`, the following values are returned based on the dimensional parameter $\boldsymbol{w}$ and the radius $r$ at each point in the design region.
- $r < w_0$ → 1
- $w_0 < r < w_0 + w_1$ → 0
- $w_0 + w_1 < r$ → -1

This assigns `level 0` material to the region where $r < w_0$, `level 1` material where $w_0 < r < w_0 + w_1$, and `level 2` material where $w_0 + w_1 < r$.

## Configurable keyword arguments
- `num_level: int` ... Number of levels to assign.
- `scale: float` ... Scale multiplied by the dimensional parameter $\boldsymbol{w}$. The default value is `1.0`.
