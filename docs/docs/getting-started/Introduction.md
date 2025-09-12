---
sidebar_position: 1
---

# Introduction
ここでは、EMOptSolutionによる形状最適化の導入を行います。

## Try Example by One Command
EMOptSolutionの形状最適化がどのように動作するか試すには、以下のコマンドを実行します。
```sh
python emopt.py run Dmodel
```
これにより、電気学会Dmodel\[1\]の単目的トポロジー最適化（NGnet on/off法\[3\]）が実行されます。
:::info
実際にこの最適化によって得られる結果の例については[Showcase](../../showcase/Dmodel.md)をご覧ください。
:::

## Basic Flow of Optimization
EMOptSolutionでは各最適化ケースを**プロジェクト単位**で管理します。プロジェクトの実体は`project`フォルダ内の各フォルダです。プロジェクトフォルダには以下のファイルが含まれます。
- **最適化に関するコンフィグ（yamlファイル）**
    - `mahcine.yaml`: 形状最適化において、最適化対象機器に関係するコンフィグ
    - `optimization_problem.yaml`: 形状最適化問題（目的関数や制約条件など）を定義するコンフィグ
    - `optimization.yaml`: 最適化の実行に関するコンフィグ（最適化イテレーション数など）
- **形状最適化のベースモデルとして用いるメッシュファイル（`pre_geom2D.msh`, `rotor_mesh2D.msh`：運動領域を含む場合）**
    - ただし、eMotorSolution連携時は不要。代わりにeMotorSolutionプロジェクトを`machine.yaml`にて指定する。
- **形状最適化解析ケースフォルダ**
    - 各解析ケースフォルダにはそれと同名のpyemsol入力jsonファイルを配置します。
    - 解析ケース名は`optimization_problem.yaml` > `case_names`コンフィグにも設定します。
    - ただし、eMotorSolution連携時は不要。代わりにeMotorSolutionプロジェクトを`machine.yaml`にて指定する。
:::info
具体的な設定方法などは[Optimization Problem](./opt_problem.md)ページおよびGuidesセクションに説明があります（ここでは省略しています）。
:::

いくつかのプロジェクト例が`project`フォルダ内にすでに配置されています。冒頭の例で指定した`Dmodel`はその一つです。

まずは、いずれかのプロジェクトを`cp_proj`コマンドにより複製するところから始めましょう。
例えば、Dmodelの最適化を別プロジェクトとして実行したい場合、以下のコマンドを実行してDmodelプロジェクトを複製します。
```sh
python emopt.py cp_proj Dmodel NewDmodel
```

コピーしたプロジェクトは`project`フォルダ内に自動的に作成されます。  
NewDmodelプロジェクトフォルダ内のファイルを編集することで、各種設定を行います。

例えば、`optimization.yaml`ファイル内の`level_set_function` > `kwargs` > `sigma` の値を以下の通りに`0.0013`から`0.0010`に変更します。  
これにより、得られるモータ形状がより複雑に変化するようになります。
```yaml
level_set_function:
  name: ngnet
  kwargs:
    sigma: 0.0010
    design_region: [[0.008, 0.0275], [0, 45.0]]
    coordinate: Polar
```
:::tip NGnetの設定
具体的には、`sigma`の値はNGnetを構成する各ガウス基底関数の標準偏差に対応します。  
デフォルトの設定では、基底関数は`design_region`を埋めるよう自動的に配置されます。 
NGnetの詳細については[Guides > LevelSetFunction > NGnet](../guides/LevelSetFunction/ngnet.md)を参照してください。
:::

最適化を実行するには、`run`コマンドを実行します。
```sh
python emopt.py run NewDmodel
```

`run`コマンドを実行すると最適化が始まると同時に、デフォルトで最適化経過をチェックするためのGUIが立ち上がります（オフにするには`optimization.yaml`内の`enable_progress_gui`を`False`に設定します）。
![GUI例](/img/GUI_ex.png)

既定の回数の最適化イテレーションが経過するか、GUI上から停止されると最適化計算が完了状態になります。完了後もGUIは自由に操作でき、GUIを閉じるかCUI（コマンドライン）上で`Ctrl+C`を入力することでプロセスを完全に終了します。

GUIは`check`コマンドによってプロセス終了後に起動することもできます。主に完了した最適化計算の振り返りに活用できます。
```sh
python emopt.py check NewDmodel
```

## Overview of GUI
![GUI（単目的最適化）](/img/GUI_soo.png)

①最適化コントロールパネル。
- `Stop`: 最適化停止
- `Pause / Resume`: 最適化中断／再開

②最適化経過グラフ。単目的最適化では最適化イテレーションー評価値グラフ、多目的最適化ではパレートフロント（3目的以上の場合、最初の2目的のみ）が表示されます。また、グラフをクリックすると、対応する形状画像が③に表示されます。

③形状画像ウィンドウ。②でクリックされた個体の形状が、`optimization_problem.yaml` > `other_metrics`に登録した関数値とともに左ウィンドウに表示されます。なお、単目的最適化の場合、イテレーション毎に最良形状が自動的に表示されます。
- `Save outcome`: 表示されている画像、および個体情報を`project`フォルダ内に保存します。
- `Pin to right`: 左ウィンドウの画像を右ウィンドウに固定します。
- `Remove pinned`: 右ウィンドウの画像を取り除きます。

④比較用のメトリクスグラフ。③に表示されている形状の`other_metrics`関数値が棒グラフで表示されます。グラフには③右ウィンドウの形状の関数値を1としたときの比率が表示されます（右ウィンドウに形状が無い場合、全メトリクスが常に1として表示されます）。
