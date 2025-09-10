---
sidebar_position: 3
---

# pyemsol_shape_evaluator
pyemsolによる形状最適化の評価実装。

## 概要
解候補ベクトルから`ls_function`や`ems_shape_builder`によって定義された形状を解析し、`optimization_problem.yaml`に定義された目的関数および制約条件を計算します。  
形状の解析は`optimization_problem.yaml` > `case_names`に定義された各解析ケースフォルダごとに独立して実行されます。解析ケースフォルダ内には同名のpyemsol入力jsonファイルが存在していることを前提とします。

## 設定可能なキーワード引数一覧
なし
