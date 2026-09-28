---
sidebar_position: 2
---

# phase_conditioner
An implementation example that dynamically configures the current phase angle.

## Overview
The current phase angle is defined from the parameter $\boldsymbol{p}=\{p_0\}$. Internally, the implementation receives pyemsol input JSON data and an analysis case name. When the analysis case name matches one of the values in `case_names`, it adds `scale`$ \times p_0$ to the phase-angle field in the JSON data.

$p_0$: Current phase angle \[deg\].  

## Configurable keyword arguments
`case_names`: List of analysis case names for which the current phase angle is changed.
`scale`: Current phase-angle scale. The default value is `1.0`.
