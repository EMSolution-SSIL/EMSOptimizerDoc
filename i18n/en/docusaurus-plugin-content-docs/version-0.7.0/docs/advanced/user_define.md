---
sidebar_position: 1
---

# Creating Custom Core Objects
This page explains how core object configuration works and how to define your own EMSOptimizer core objects.

## Procedure
**Follow these steps to define a custom core object.**  
1. Create a new Python file for the custom core object.
2. In the file, implement a Python class that inherits the interface for the corresponding core object (the example below is for `evaluator`).
```py
class UserDefinedEvaluator(EvaluatorInterface):
    def __init__(self, kwarg1: int): ...
```
:::info
See the page for each core object in the User Guide for its interface.
:::
3. In the file, define a factory function that instantiates the corresponding core object and is decorated for core-object creation.
```py
from emsopt_engine.registry import evaluator


@evaluator("user_defined_evaluator")
def build_user_defined_evaluator(kwarg1: int) -> EvaluatorInterface:
    return UserDefinedEvaluator(kwarg1)
```
4. Import the Python file in `implementations.py` inside the corresponding core object folder.
```py
from .examples import rastrigin, zdt1, user_defined
```

Following these steps makes the custom core object available like the other core object examples: specify its `name` (in this example, `user_defined_evaluator`) and keyword arguments in `optimization.yaml`. 
```yaml
evaluator:
  name: user_defined_evaluator
  kwargs:
    kwarg1: 1
```
:::info
The existing implementation examples are also created using this procedure.  
If you are unsure how to create a core object, refer to an existing implementation example.
:::

## How Core Objects Work
This section describes how core object configuration works and provides implementation tips.
### Interface
The specifications of core objects are defined by interface classes. For example, the interface class for `evaluator` (`EvaluatorInterface`) is defined as follows.
```py
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
    def evaluate_parallel(
        self, population: Population, num_processes: int | None = None
    ) -> Population:
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
**Users must inherit from `EvaluatorInterface` and implement all methods defined by the interface according to their specifications**.

EMSOptimizer checks in several places that core object implementations conform to their corresponding interfaces. Conversely, **if a custom core object conforms to its interface, EMSOptimizer can immediately integrate with it**.

### Registering Core Objects
Internally, EMSOptimizer maintains a registry of core objects (more precisely, factory functions that create core object instances). **Custom core objects must be registered to be used**.
:::tip[How the registry works]
At runtime, EMSOptimizer:
- searches the registry for the name configuration set for each core object in `optimization.yaml`,
- calls the factory function corresponding to that `name`, passing the `kwargs` configuration as keyword arguments, and
- uses the core object created by the factory function in the optimization calculation.

Names not registered in the registry cannot be used as core objects.
:::

Factory functions are registered in the registry using decorator functions available from `emsopt_engine.registry`. The `str` argument passed to a decorator becomes the registration name.  
In the example above,
```py
from emsopt_engine.registry import evaluator


@evaluator("user_defined_evaluator")
def build_user_defined_evaluator() -> EvaluatorInterface:
    return UserDefinedEvaluator()
```
`@evaluator` is the decorator function for registering an object in the `evaluator` registry, `user_defined_evaluator` is the registration name, and `build_user_defined_evaluator()` is the factory function for the custom core object.

**The Python file must be imported to trigger the decorator function.** This is done in `implementations.py` inside each core-object folder.
```py
from .examples import rastrigin, zdt1, user_defined
```
`implementations.py` is loaded automatically when EMSOptimizer runs. The decorator is triggered at that time, registering the factory function in the registry.

### About optimizer
Among the core objects, **`optimizer` is somewhat special**:
- In addition to the interface (`OptimizerInterface`), it inherits one of the following base classes:
    - single-objective optimization base class (`SOOptimizerBase`)
    - multi-objective optimization base class (`MOOptimizerBase`)
- When defining a custom `optimizer`, users **must inherit one of these base classes in addition to the interface**.
- The keyword arguments `dim` and `num_obj` are automatically passed to the factory function. Therefore, **an `optimizer` factory function must accept `dim` and `num_obj`**.
:::info
This automatic argument configuration dynamically sets `dim` and `num_obj` during shape optimization. EMSOptimizer calculates and sets these arguments internally so that they remain consistent with other core objects and settings such as `optimization_problem.yaml`.
:::

#### Example
As an example, consider the `cmaes` implementation (partially omitted).
```py
import numpy as np
from cmaes import CMA

from core.individual import Individual, Population
from core.optimizer.optimizer_interface import OptimizerInterface
from core.optimizer.so_optimizer_base import SOOptimizerBase
from emsopt_engine.registry import optimizer


class CMAES(SOOptimizerBase, OptimizerInterface):
    def __init__(
        self,
        dim: int,
        mean: np.ndarray | None = None,
        sigma: float = 1.0,
        bounds: tuple[float, float] | list[tuple[float, float]] | None = None,
        seed: int | None = None,
        population_size: int | None = None,
    ) -> None: ...
```
- Because `cmaes` is a single-objective optimization algorithm, its implementation inherits `SOOptimizerBase`. `SOOptimizerBase` implements mechanisms such as elite-solution management, which are also available inside the `CMAES` class.
```py
@optimizer("cmaes")
def build_cmaes(
    dim: int,
    num_obj: int,
    mean: np.ndarray | None = None,
    sigma: float = 1.0,
    bounds: tuple[float, float] | list[tuple[float, float]] | None = None,
    seed: int | None = None,
    population_size: int | None = None,
) -> OptimizerInterface:
    return CMAES(
        dim=dim,
        mean=mean,
        sigma=sigma,
        bounds=bounds,
        seed=seed,
        population_size=population_size,
    )
```
- The factory function accepts `dim: int` and `num_obj: int` as keyword arguments. `num_obj` is not used by the `CMAES` class because it is unnecessary for its processing, but it must exist as a keyword argument to satisfy the `optimizer` factory contract.  
Multi-objective optimizer implementations can use `num_obj` as the number of objectives for various operations.

## Defining custom shape-optimization evaluation functions
Evaluation functions for shape optimization that can be configured in `optimization_problem.yaml` are implemented in `core/opt_problem_functions.py`. These functions are also registered in a system similar to that used for core objects, so users can create and register their own evaluation functions.

The following is an implementation example for `average_torque` (the average-torque evaluation function).
```py
@opt_problem_function("average_torque")
def average_torque(working_dir: str, torque_scale: float = 1.0) -> float:
    """
    Calculate the average value of the torque waveform.
    Args:
        working_dir (str): Directory containing analysis result json file
        torque_scale (float, optional): Torque scale factor. Defaults to 1.0.
    Returns:
        float: Average torque value
    """
    json_path = Path(working_dir) / "output.json"
    with json_path.open(encoding="utf-8") as f:
        result = json.load(f)
    torque_wave = np.array(
        [
            item["forceMZ"]
            for item in result["postData"]["forceNodal"]["forceNodalData"]
            if item["propertyNum"] == "rotor"
        ][0]
    )
    torque_wave *= torque_scale
    res = np.mean(torque_wave)
    return res
```

As with registering a core-object factory function, pass the registration name of the custom function to the `opt_problem_function` decorator to make the function callable from `optimization_problem.yaml`. No additional import is required because `core/opt_problem_functions.py` itself is automatically imported by EMSOptimizer.

Note that **evaluation functions must always include `working_dir` as their first argument**. This is the directory containing the analysis results from pyemsol/eMachineSim, and it is set automatically inside EMSOptimizer.  
The `average_torque` example above reads the pyemsol/eMachineSim result-summary file `output.json`, extracts the torque waveform, and calculates its average.
