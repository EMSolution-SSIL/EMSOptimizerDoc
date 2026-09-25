---
sidebar_position: 1
---

# インターフェース
Evaluatorのインターフェース定義（`EvaluatorInterface`）は以下の通りです。  
`emsopt_engine.interface.evaluator_interface`からimportできます。

```py
from abc import ABC, abstractmethod

from emsopt_engine.individual import Population


class EvaluatorInterface(ABC):
    """Interface to evaluate population"""

    @abstractmethod
    def evaluate(self, population: Population) -> Population:
        """Evaluate individuals
        Args:
            population: Population instance
        Returns:
            Population with metrics values set
        """

    @abstractmethod
    def evaluate_parallel(self, population: Population, num_processes: int | None = None) -> Population:
        """Evaluate individuals (parallelized)
        Args:
            population: Population instance
            num_processes: Number of processes. If None, automatically set from CPU info (multiprocessing.cpu_count()).
        Returns:
            Population with metrics values set
        """

    @abstractmethod
    def get_variable_dimension(self) -> int:
        """Get variable dimension

        Returns:
            int: dimension
        """

    @abstractmethod
    def get_num_objectives(self) -> int:
        """Get number of objectives

        Returns:
            int: number of objectives
        """
```
