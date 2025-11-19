---
sidebar_position: 11
---

# eMotorSolutionとの連携
ここでは、モータ設計およびシミュレーションツール「eMotorSolution」との機能連携について説明します。

## 連携の有効化
eMotorSolutionとの連携を有効化するには、**eMotorSolution APIをpython環境にインストールしたうえで、以下の設定を行います**。
- `machine.yaml` > `ems_project_filepath`に連携したいeMotorSolutionプロジェクトファイル（json）のパスを設定する。
- 環境変数`GMSH_EXE_PATH`にメッシュ生成ツールgmsh\[14\]の実行ファイルのパスを設定する。
:::info
eMotorSolution APIのインストール方法については[インストール](../intro.md)ページを参照してください。
:::
:::info
eMotorSolution APIはデフォルトのメッシュ生成ツールとしてgmshを外部呼出しします。連携時はgmshの実行ファイルをダウンロードして環境変数`GMSH_EXE_PATH`にパスの設定を行ってください。
:::

## 機能一覧
### 寸法最適化
eMotorSolutionと連携時、コアオブジェクト`ems_shape_builder`による寸法最適化が実施可能です。また、eMotorSolution連携時はeMotorSolution API経由でメッシュが動的に生成されます（したがって、EMSOptimizerプロジェクトフォルダにメッシュファイルは不要となります）。
:::info
寸法最適化の設定方法については[基本の使い方 > EMSOptimizerのコンセプト](../getting-started/core_concepts.md)ページ、[ユーザガイド > 最適化の設定](./optimization_config.md)ページ、ユーザガイド > eMotorSolution Shape Builderセクションなどを参照してください。
:::

### Analysis Case Control
eMotorSolutionと連携時は形状解析時、連携先プロジェクトの解析ケースフォルダを参照します。したがって、EMSOptimizerプロジェクトフォルダに解析ケースフォルダは不要となります。
:::warning
解析ケース名は未連携時と同じく、`optimization_problem.yaml` > `case_names`に正しく設定してください。
:::
