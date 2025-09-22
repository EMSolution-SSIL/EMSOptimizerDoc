---
sidebar_position: 3
---

# NGnet
NGnet実装です。NGnet on/off法\[3\]において形状表現に用いられます。

## 概要
NGnet $y(\boldsymbol{w}, \boldsymbol{x})$は以下の通り定義されます（2次元座標空間の場合）。
```math
y(\boldsymbol{w}, \boldsymbol{x}) = \sum_{i=1}^{N} w_i b_i(\boldsymbol{x}) \\
b_i(\boldsymbol{x}) = \frac{G_i(\boldsymbol{x})}{\sum_{j=1}^N G_j(\boldsymbol{x})} \\
G_i(\boldsymbol{x}) = \frac{1}{2\pi \sigma_i^2}\exp(-\frac{\|\boldsymbol{x}-\boldsymbol{\mu_i}\|^2}{2\sigma_i^2}) \\
\boldsymbol{w} = \{w_i\}, \boldsymbol{x} = \{x, y\}
```
$\boldsymbol{w}$: 重みベクトル  
$\boldsymbol{x}$: 座標ベクトル  
$N$: NGnetを構成するガウス基底関数の数  
$\mu_i$: $i$番目ガウス基底関数$G_i(\boldsymbol{x})$の中心ベクトル  
$\sigma_i$: $i$番目ガウス基底関数$G_i(\boldsymbol{x})$の標準偏差

NGnet on/off法では、重みベクトル$\boldsymbol{w}$を最適化することで$y(\boldsymbol{w}, \boldsymbol{x})$の分布を変化させ、その値に従って設計領域の各位置$\boldsymbol{x}$における材料種を決定します。  
原著論文では$y(\boldsymbol{w}, \boldsymbol{x})$が0より大きい箇所をON材料（磁性体コア）、0以下の箇所をOFF材料（空気）と定義しています。

## 設定可能なキーワード引数一覧
- `coordinate: str` ... NGnetの構築に用いる座標系。 "Cartesian"または"Polar"。
- `sigma: float` ... NGnetを構成するガウス基底関数の標準偏差。デフォルト値は`1`。
- `design_region: list[list[float, float], list[float, float]]` ... NGnetを構築する範囲（＝設計領域）。`coordinate`が`Cartesian`の場合は矩形領域$[[x_1, x_2], [y_1, y_2]]$、`Polar`の場合は扇状領域$[[r_1, r_2], [\theta_1, \theta_2]]$を設定します。
:::tip ガウス基底関数の配置
デフォルトの設定では、NGnetを構成するガウス基底関数は下図のように`design_region`を埋めるように自動的に配置されます。  
下図において各円がガウス基底関数の配置を表しており、その半径は標準偏差を表しています。この図は形状最適化実行時に`gaussian.png`という名前でEMSOptimizerフォルダ直下に出力されます。  
![ガウス基底関数の配置](/img/gaussian_arrangement.png)
:::
