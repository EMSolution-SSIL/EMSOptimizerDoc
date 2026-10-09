---
sidebar_position: 1
---

# Interface
The interface definition for Level Set Function (`LevelSetFunctionInterface`) is shown below.  
It can be imported from `emsopt_engine.interface.level_set_function_interface`.

```py
from abc import ABC, abstractmethod

import numpy as np


class LevelSetFunctionInterface(ABC):
    """Level set function interface"""

    @abstractmethod
    def get_variable_dimension(self) -> int:
        """Get variable dimension

        Returns:
            int: dimension
        """

    @abstractmethod
    def calculate_output(self, parameters: np.ndarray, points: np.ndarray) -> np.ndarray:
        """Batch compute the output of the level set function defined by parameters at points

        Args:
            parameters (np.ndarray): K-dimensional vector (K: number of parameters of the level set function)
            points (np.ndarray): 2D array (N points * D dimensions), each row corresponds to a calculation point

        Returns:
            Output calculation result (N-dimensional vector)
        """
```
