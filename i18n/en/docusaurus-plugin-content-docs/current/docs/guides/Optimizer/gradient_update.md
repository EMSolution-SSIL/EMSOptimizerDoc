---
sidebar_position: 6
---

# gradient_update
This is an implementation of a gradient-based update algorithm. It assumes that `level_set_function` is `pyemsol_desity`.

## Overview
In gradient-based methods, the design variables $\boldsymbol{x}$ (often the density or level set value of each cell in the design region) are updated from the gradient of the objective function $f$ as follows (assuming a minimization problem)\[12\], \[26\], \[27\], \[31\].  
```math
\boldsymbol{x} \leftarrow \boldsymbol{x} - \alpha \frac{\partial f}{\partial \boldsymbol{x}}
```
Here, $\alpha$ denotes the step size.  
Methods based on the phase-field diffusion-reaction equation also include a diffusion term (the Laplacian of the design variables). The diffusion term is known to affect the complexity of the resulting shape\[28\]-\[30\].
```math
\boldsymbol{x} \leftarrow \boldsymbol{x} + \alpha \left(-M \frac{\partial f}{\partial \boldsymbol{x}} + \tau \nabla^2 \boldsymbol{x}\right)
```

## Configurable keyword arguments
- `init_uniform_value: float` ... Initial value of the design variables. This value is assigned to all design variables.
- `init_value_filepath: str | null` ... File path containing the initial design variables. When specified, this takes precedence over `init_uniform_value`.
- `bounds: tuple[float, float] | null` ... Lower and upper bounds for the design variables. When `null`, \[-1,1\] is set automatically.
- `step_size: float` ... Step size $\alpha$. The default is `1.0`.
- `reaction_coef: float` ... Reaction-term coefficient $M$\[28\]-\[30\]. The default is `1.0`.
- `diffusion_coef: float` ... Diffusion-term coefficient $\tau$\[28\]-\[30\]. The default is `1.0`.
- `move_limit: float` ... Move limit\[31\]. Limits the change in a design variable during one update to \[-move_limit, +move_limit\]. The default is `0.2`.
- `damping_factor: float` ... Move-limit damping factor\[31\]. When the objective value worsens, multiplying the move limit by this factor suppresses objective oscillation (repeated improvement and deterioration without convergence). The default is `0.99`.
- `scaling_mode: str` ... Gradient scaling mode. `none`: use the gradient obtained from the analysis as-is. `max`: scale the gradient using the bounds and maximum value. `sign`: use only the sign of the gradient and set the upper bound for a positive sign or the lower bound for a negative sign. In all modes, however, the change in the design variables is limited by `move_limit`.
- `constraint_mode: str` ... Constraint mode. `none`: no constraint. `volume_penalty`: volume constraint.
- `volume_frac_ulim: float` ... Upper limit (fraction) for the volume constraint. For `0.5`, the integrated material density is constrained to be at most 50% of the entire design region.
- `volume_penalty_coef: float` ... Penalty coefficient for constraint violations when constraint_mode is `volume_penalty`. The gradient is adjusted so that the overall density decreases by the constraint violation multiplied by this coefficient.
