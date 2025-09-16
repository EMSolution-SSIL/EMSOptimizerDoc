---
sidebar_position: 8
---

# How to Define Core Object
ここでは、コアオブジェクト設定の仕組みとユーザ自身がEMOptSolutionのコアオブジェクトを定義する方法を説明します。

## Steps to Define Core Object in Short
**自作コアオブジェクトを定義するには、以下のステップに従います**。  
1. 自作コアオブジェクト用の新しいpythonファイルを作成する。
2. 作成したファイル内に、対応するコアオブジェクトインターフェースを継承したpythonクラスを実装する（下記は`evaluator`の例）。
```py
class UserDefinedEvaluator(EvaluatorInterface):
    def __init__(self, kwarg1: int):
        ...
```
3. 作成したファイル内に、対応するコアオブジェクト生成用デコレータ付きのインスタンス化関数（ファクトリ関数）を定義する。
```py
from proprietary_free.registry import evaluator
@evaluator("user_defined_evaluator")
def build_user_defined_evaluator(kwarg1: int) -> EvaluatorInterface:
    return UserDefinedEvaluator(kwarg1)
```
4. 作成したpythonファイルを各コアオブジェクトフォルダ内の`implementations.py`内でインポートする。
```py
from .examples import rastrigin, zdt1, user_defined
```

以上の手続きによって、ほかのコアオブジェクト実装例と同様に`optimization.yaml`にて名前（上記の例では`user_defined_evaluator`）とキーワード引数を指定することで自作コアオブジェクトを利用できるようになります。 
```yaml
evaluator:
  name: user_defined_evaluator
  kwargs:
    kwarg1: 1
```
:::info
既存の実装例も上記の手続きによって作成されてます。  
コアオブジェクトの作成手順に迷った場合は、既存の実装例をご覧ください。
:::

## Configuration System of Core Object
ここでは、コアオブジェクト設定の仕組みと実装のヒントについて述べます。
### Interface
コアオブジェクトの仕様はインターフェースクラスによって定義されています。例えば、`evaluator`のインターフェースクラス（`EvaluatorInterface` in `core/evaluator/evaluator_interface.py`）の定義は下記のようになっています。
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
**ユーザは`EvaluatorInterface`を継承し、なおかつインターフェース内で定義されたすべてのメソッドを定義通りに実装する必要があります**。

EMOptSolution内部では、各種コアオブジェクト実装が対応するインターフェースに沿っているかをチェックする機構が各所に施されています。逆に言えば、**自作コアオブジェクトの実装がインターフェースに沿っていれば、EMOptSolutionは即座にオブジェクトと連携することが可能です**。

### Registration of Core Object
EMOptSolutionは内部的にコアオブジェクト（正確にはコアオブジェクトインスタンスを生成するファクトリ関数）のレジストリを保持しています。**自作コアオブジェクトを利用するためにはレジストリへの登録が必要です**。
:::tip レジストリの仕組み
EMOptSolutionは実行時、
- `optimization.yaml`内で各コアオブジェクトに設定した`name`コンフィグをレジストリ内検索し、
- `kwargs`コンフィグをキーワード引数として、`name`コンフィグに該当するファクトリ関数を呼び出し、
- ファクトリ関数によって生成されたコアオブジェクトを最適化計算に利用する

仕組みとなっています。レジストリに未登録の名前はコアオブジェクトとして使用できません。
:::

レジストリへのファクトリ関数の登録は`proprietary_free.registry`から呼び出せる各種デコレータ関数によって行います。デコレータ関数への引数（`str`型）がそのままレジストリへの登録名になります。  
冒頭の例では、
```py
from proprietary_free.registry import evaluator
@evaluator("user_defined_evaluator")
def build_user_defined_evaluator() -> EvaluatorInterface:
    return UserDefinedEvaluator()
```
となっており、`@evaluator`が`evaluator`レジストリ登録用のデコレータ関数、`user_defined_evaluator`が登録名、`build_user_defined_evaluator()`が自作コアオブジェクトのファクトリ関数です。

**デコレータ関数をトリガーするためにはそのpythonファイルをインポートする必要があります**。これは各コアオブジェクトフォルダ内の`implementations.py`内で行います。
```py
from .examples import rastrigin, zdt1, user_defined
```
`implementations.py`はEMOptSolution実行時に自動的に読み込まれ、このときにデコレータ関数がトリガーされることでファクトリ関数がレジストリへ登録される仕組みになっています。

### Important Notice for Optimizer
コアオブジェクトのうち、**`optimizer`は少し特殊なオブジェクトとなっています**。すなわち、
- 継承元としてインターフェース（`OptimizerInterface` in `core/optimizer/optimizer_interface.py`）のほかに、
    - 単目的最適化の基底クラス（`SOOptimizerBase` in `core/optimizer/so_optimizer_base.py`）
    - 多目的最適化の基底クラス（`MOOptimizerBase` in `core/optimizer/mo_optimizer_base.py`）
- を有している。ユーザは`optimizer`を自作する際、**インターフェースに加えてどちらかの基底クラスを継承する必要がある**。
- 形状最適化実行時（`pyemsol_shape_evaluator`使用時）、ファクトリ関数へ`dim`と`num_obj`というキーワード引数が自動的に設定される。したがって、**`optimizer`のファクトリ関数は`dim`と`num_obj`を引数に設定する必要がある**。
:::info
この引数の自動設定の仕組みは、「形状最適化時に`dim`と`num_obj`を動的に設定する」ためのものです。ほかのコアオブジェクトや`optimization_problem.yaml`などの設定と齟齬が生じないよう、EMOptSolutionが内部でこれらの引数を自動的に計算・設定します。
:::

#### Example
例として、`cmaes`実装を見てみましょう（一部省略）。
```py
import numpy as np
from cmaes import CMA

from core.individual import Individual, Population
from core.optimizer.optimizer_interface import OptimizerInterface
from core.optimizer.so_optimizer_base import SOOptimizerBase
from proprietary_free.registry import optimizer


class CMAES(SOOptimizerBase, OptimizerInterface):
    def __init__(
        self,
        dim: int,
        mean: np.ndarray | None = None,
        sigma: float = 1.0,
        bounds: tuple[float, float] | list[tuple[float, float]] | None = None,
        seed: int | None = None,
        population_size: int | None = None,
    ) -> None:
        ...
```
- `cmaes`実装は単目的最適化アルゴリズムであるため、`SOOptimizerBase`を継承しています。`SOOptimizerBase`にはエリート解管理の仕組みなどが実装されており、その仕組みは`CMAES`クラス内でも利用可能です。
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
- `dim: int`, `num_obj: int`をファクトリ関数のキーワード引数に受け取っています。このうち`num_obj`は`CMAES`クラスの処理には不要であるため特に使われていません（`optimizer`ファクトリ関数の契約上、キーワード引数としては存在しなければならない）。  
多目的最適化実装においては`num_obj`を目的関数の数として各種処理に利用できます。

## Definition of Optimization Problem Function
`optimization_problem.yaml`に設定できる形状最適化時の評価用関数は`core/opt_problem_functions.py`に実装があり、これらの関数もコアオブジェクトと類似のシステムによってレジストリへ登録されています。したがって、ユーザは自作の評価用関数を作成・登録することも可能です。

以下は`average_torque`（平均トルク評価関数）の実装例です。
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

コアオブジェクトのファクトリ関数の登録時と同様に、デコレータ関数`opt_problem_function`に自作関数の登録名を渡すことで`optimization_problem.yaml`からその関数を呼び出せるようになります（`core/opt_problem_functions.py`自身がEMOptSolutionに自動インポートされるため、追加のインポート記述は不要です）。

なお、**評価用関数には`working_dir`を引数に必ず含みます**。これはpyemsolによる解析結果が格納されたフォルダ名であり、EMOptSolution内部で自動的に設定されます。  
上記の`average_torque`の例ではpyemsol解析結果サマリーファイル`output.json`を読み込み、そこからトルク波形を抽出することで平均トルクを計算しています。
