---
sidebar_position: 1
---

# Interface
The interface definition for eMotorSolution Shape Builder (`EMSShapeBuilderInterface`) is shown below.  
It can be imported from `emsopt_engine.interface.ems_shape_builder_interface`.

```py
from abc import ABC, abstractmethod

import numpy as np


class EMSShapeBuilderInterface(ABC):
    """Shape builder interface using eMotorSolution API"""

    @abstractmethod
    def get_variable_dimension(self) -> int:
        """Get variable dimension

        Returns:
            int: dimension
        """

    @abstractmethod
    def update_shape(self, parameters: np.ndarray, project: object) -> bool:
        """Update shape from parameters

        Args:
            parameters (np.ndarray): K-dimensional vector (K: number of parameters for shape design)
            project (object): eMotorSolution Project instance. For detail, please refer to eMotorSolution's API website.

        Returns:
            bool: True if succeeded, False otherwise
        """
```
