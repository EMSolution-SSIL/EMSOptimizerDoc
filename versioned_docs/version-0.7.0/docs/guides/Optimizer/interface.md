---
sidebar_position: 1
---

# インターフェース
Optimizerのインターフェース定義（`OptimizerInterface`）は以下の通りです。  
`emsopt_engine.interface.optimizer_interface`からimportできます。

```py
from abc import ABC, abstractmethod

from emsopt_engine.individual import Population

class OptimizerInterface(ABC):
    """Interface for optimization"""

    @abstractmethod
    def get_population(self) -> Population | None:
        """Retrieves the population
        Returns:
            Population
        """

    @abstractmethod
    def setup_population(self, evaluated_population: Population) -> None:
        """Performs initial setup of the population (for population-based optimization methods)
        Args:
            evaluated_population: Population with evaluated individuals
        """

    @abstractmethod
    def get_candidates(self) -> Population:
        """Retrieves the candidates to be evaluated
        Returns:
            Population
        """

    @abstractmethod
    def proceed_to_next_iteration(self, evaluated_candidates: Population) -> None:
        """Updates the population and proceeds to the next iteration
        Updates individuals according to the optimization algorithm and moves to the next generation.
        Args:
            evaluated_candidates: Candidate population with evaluation values
        """
```
