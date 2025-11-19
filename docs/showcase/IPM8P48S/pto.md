---
sidebar_position: 2
---

# IPM8P48S寸法およびトポロジー同時最適化
ここでは`IPM8P48S_pto`プロジェクトの内容について紹介します。  
このプロジェクトでは、IPM8P48Sモデルの寸法およびトポロジーの同時最適化を実行します。
:::info
本プロジェクトの最適化の実施にはeMotorSolution APIが必要です。
:::

## 最適化概要
`IPM8P48S_pto`プロジェクトでは下図のように、ロータの部品構造（永久磁石＋フラックスバリア）は寸法パラメータによって表現し、ロータ表面の細かいトポロジーはNGnet on/off法によって決定します。  
ロータ表面構造は特にトルクリプルに寄与することが一般に知られています。そのため、本最適化ではトルクリプルの最小化を目的として、部品構造には単純な寸法パラメータを採用しつつ、新規的なロータ表面の構造の獲得を狙います。  
![IPM8P48S PTO説明](/img/IPM8P48S_pto_ex.png)

## machine.yaml（`IPM8P48S_pto`プロジェクト）
`machine.yaml`の基本設定は`IPM8P48S_moo`プロジェクトと同じですが、eMotorSolutionと連携して寸法最適化を行うため、`ems_project_filepath`コンフィグを追加します。  
`IPM8P48S_pto`プロジェクトにはすでにeMotorSolutionプロジェクトjsonファイルが含まれているため、そのファイルパスを指定します。  
```yaml
# ems functionality link
ems_project_filepath: "Path/To/EMSOptimizer/projects/IPM8P48S_pto/IPM8P48S.json"
```
:::info
上記のファイルパスはご使用のEMSOptimizerのインストール先に合わせて設定してください。
:::

### Implicit Domain Meshing オプション
冒頭で述べた通り、今回はロータ表面のみを細かくトポロジー最適化によって変形させます。  
このような場合、Implicit Domain Meshingではメッシュが細かくなりすぎる可能性があるため、`IPM8P48S_pto`プロジェクトではデフォルトでオフにしています。

## optimization.yaml（`IPM8P48S_pto`プロジェクト）
まず、形状決定にかかわるオブジェクトから説明します。  
レベルセット関数に`ngnet_mixture`を設定し、半径78.2mm以上（からロータ半径である80.2mm以下）の範囲に限ってNGnet on/off法によるトポロジー最適化を実施します。  
同時に、`ems_shape_builder`を`HoleMagnet55`に設定しています。これは、IPM8P48Sオリジナルモデルにも使用されているeMotorSolution Hole Magnet Type55（ロータ永久磁石＋フラックスバリアモデル）の寸法を10の設計変数から設定するオブジェクトです。  
これを`level_set_function`と同時に設定することで、
- ロータの部品構造は`HoleMagnet55`によって決定し、
- ロータ表面の細かいトポロジーの修正はNGnet on/off法により行う  
という形状決定が行われます。
```yaml
level_set_function:
  name: ngnet_mixture
  kwargs:
    sigma: 0.001
    design_region: [[0.0782, 0.0802], [0, 22.5]]
    coordinate: Polar
    boundary_r: 0.0782
    inversed: True
ems_shape_builder:
  name: HoleMagnet55
```

今回は単目的形状最適化を行うため、最適化手法に`cmaes`を設定しています。  
ここで、`bounds`に設定しているのは`HoleMagnet55`寸法パラメータの上下限値です。IPM8P48Sのオリジナルモデルを参考に設定しています。
```yaml
evaluator:
  name: pyemsol_shape_evaluator
optimizer:
  name: cmaes
  kwargs:
    seed: 42
    bounds: [[40, 45], [1.5, 2.5], [1.0, 2.0], [11, 13], [20, 22],
             [16, 20], [1.0, 2.0], [0.5, 1.5], [4.0, 6.0], [0.0, 1.0]]
```
:::tip 解析条件・寸法・トポロジーの同時最適化
今回のケースでは`ems_shape_builder`を`ls_function`と同時に設定することで、寸法・トポロジーの同時最適化\[10\]を実行します。このとき、解候補ベクトルは以下のように構成されます。
```math
\boldsymbol{x} = [\boldsymbol{d}^\text{T}, \boldsymbol{w}^\text{T}]^\text{T}
```
$\boldsymbol{x}$: 解候補ベクトル（`Individual.solution`）  
$\boldsymbol{d}$: `ems_shape_builder`に与えられる寸法情報ベクトル  
$\boldsymbol{w}$: `ls_function`に与えられるレベルセット関数パラメータベクトル

`bounds`は今回10次元ベクトルの$\boldsymbol{d}$に対する上下限値を設定しています。なお、設定されなかった$\boldsymbol{w}$の上下限値は自動的に\[-1, 1\]に設定されます。
:::

## optimization_problem.yaml（`IPM8P48S_pto`プロジェクト）
最適化問題は以下の通りです。ここでは、平均トルクがオリジナルモデルの値14.62Nmを下回らないようにトルクリプルを最小化します。また、ロータコアの結合制約も考慮しています。
```math
\begin{align*}
\text{minimize} \quad & f_1=T_\text{rip} \\
\text{subject to} \quad & g_1=-(T_\text{avg}-14.62) \leq 0 \\
                        & h_1=N-1 = 0 \\
\end{align*}
```
$T_\text{avg}$：平均トルク [Nm]  
$T_\text{rip}$：トルクリプル率 [%]  
$N$: 連結成分数

## 最適化の実施例
形状の進化経過を以下に示します。ロータ部品構造と表面構造が同時に変化しながら、徐々に一定の構造に収束していく様子が分かります。    
![IPM8P48S PTO進化履歴](/img/IPM8P48S_pto_best_individuals.gif)

100イテレーション最適化完了後のGUIを以下に示します。目的関数値は80イテレーションほどでほぼ横ばいになっており、最適化が収束したと判断できます。  
最良形状（81イテレーション目）はオリジナルモデルに類似した永久磁石＋フラックスバリア構造を有している一方、ロータ表面がトポロジー最適化によって特徴的な構造となっていることが分かります。平均トルク: 15.597 Nm、トルクリプル率: 12.578 %。  
[多目的トポロジー最適化](./basic_moo.md)の結果ではトルクリプル率の最小値が20%程度だったことを考えると、このロータ表面の構造によってトルクリプルを低減している可能性があると判断できます。  
![IPM8P48S PTO結果](/img/IPM8P48S_pto_check.png)
