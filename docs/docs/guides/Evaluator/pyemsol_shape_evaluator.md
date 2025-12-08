---
sidebar_position: 5
---

# pyemsol_shape_evaluator
pyemsolによる形状最適化の評価実装。

## 概要
以下の条件下で形状評価を行います。ただし、`ls_function`, `ems_shape_builder`, `analysis_conditioner`がそれぞれ未設定の場合はそれに関連する処理は無視されます。
- 形状は`ls_function`および`ems_shape_builder`に解候補ベクトルを与えることで決定
- 解析条件は`analysis_conditioner`に解候補ベクトルを与えることで決定
- 目的関数および制約条件は`optimization_problem.yaml`に定義されたものを計算
- 形状の解析は`optimization_problem.yaml` > `case_names`に定義された各解析ケースごとに独立して実行されます。プロジェクトフォルダ内の各解析ケースフォルダに同名のpyemsol入力jsonファイルが存在していることを前提とします。

## 設定可能なキーワード引数一覧
なし
