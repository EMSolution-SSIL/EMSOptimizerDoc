---
sidebar_position: 1
---

# インターフェース
eMotorSolution Shape Builderのインターフェース定義（`AnalysisConditionerInterface`）は以下の通りです。  
`emsopt_engine.interface.analysis_conditioner_interface`からimportできます。

```py
from abc import ABC, abstractmethod

import numpy as np


class AnalysisConditionerInterface(ABC):
    """Analysis conditioner interface"""

    @abstractmethod
    def get_variable_dimension(self) -> int:
        """Get variable dimension

        Returns:
            int: dimension
        """

    @abstractmethod
    def condition_analysis_case(self, parameters: np.ndarray, input_json: dict, case_name: str) -> dict:
        """condition analysis case by modifing input_json

        Args:
            parameters (np.ndarray): K-dimensional vector (K: number of parameters)
            input_json (dict): pyemsol input json data
            case_name (str): Analysis case name

        Returns:
            dict: Modified input_json
        """
```
