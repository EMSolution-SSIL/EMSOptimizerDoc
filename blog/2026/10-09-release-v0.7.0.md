---
slug: release-v0.7.0
title: Release V0.7.0
authors: [SSIL]
tags: [change_log]
---

v0.7.0のリリース情報です。

{/* truncate */}

## v0.7.0 プレリリース情報
v0.7.0をリリースしました。
主要な更新内容は以下の通りです。

### 新規機能関連
- eMachineSimとの連携
    - 電気機器周辺解析用ツールeMachineSimとの連携をサポートしました。
    - pyemsolと同様に解析ケースフォルダを配置し、`optimization_problem.yaml`にて指定することで解析可能になります。
- [スタディコントロールと結果確認](/docs/next/docs/guides/study_control_and_results)
    - スタディ作成機能を追加しました。これにより，ある設計対象に対する最適化設定を複数保持できるようになりました。
    - また，各スタディの実行結果はランという単位で保存され，あとから参照できるようになりました。
- 勾配ベース手法の実装例（[勾配用optimizer](/docs/next/docs/guides/Optimizer/gradient_update), [密度表現level_set_function](/docs/next/docs/guides/LevelSetFunction/pyemsol_density)）
    - 勾配用optimizerは勾配情報に基づき，設計変数（設計要素内の各セルの密度／レベルセット値）を更新します。
    - 密度表現level_set_functionはpyemsol用に定義された特殊なオブジェクトであり，pyemsol内部にて勾配計算を実行させるトリガーとなります。
- optimizer実装例の追加（[moead](/docs/next/docs/guides/Optimizer/moead), [ga](/docs/next/docs/guides/Optimizer/ga), [sa-nsga2](/docs/next/docs/guides/Optimizer/sa_nsga2)）
- ems_shape_builder実装例の追加（[Dmodel_mixed_builder](/docs/next/docs/guides/EMSShapeBuilder/Dmodel_mixed)）
- [コマンド](/docs/next/docs/guides/commands)の更新
- [最適化設定](/docs/next/docs/guides/optimization_config)の更新
    - 出力設定の追加
    - リスタート機能
- [機器設定](/docs/next/docs/guides/machine_config)の更新
    - 画像出力設定
    - 3次元最適化の解析
    - レベルセット関数計算の設定
- [評価関数実装例](/docs/next/docs/guides/opt_problem_ex)の更新
- [サロゲートモデル導入](/docs/next/docs/advanced/surrogate_model_usage)の追加
- [AIを活用したコンフィグ設定](/docs/next/docs/advanced/ai_usage)の追加

### 主要な更新・追加
- [イントロダクション](/docs/next/docs/getting-started/Introduction)の更新
    - スタディ等について記述を追加しました。
    - GUIを更新しました。
- [最適化問題の設定](/docs/next/docs/guides/optimization_problem_config)の追加
    - [最適化問題の定義](/docs/next/docs/getting-started/opt_problem)ページの内容を，コンフィグスキーマとして正式に記述しました。
- [EMSOptimizer Python API](/docs/next/docs/guides/emsopt_api)の追加
    - v0.7.0より、最適化実行モジュール（クラス）をAPIとしても提供しています。
- [マルチマテリアル最適化実装例](/docs/next/docs/guides/LevelSetFunction/ngnet_multi_material)
    - 4,5材料表現の追加

### Showcase関連
- [Dmodel 混合変数最適化](/docs/next/showcase/Dmodel/mixed_variables)の追加
    - 永久磁石材料，コイル巻数，永久磁石寸法パラメータ，磁性体コアトポロジーを含む混合変数の最適化事例です。
- Dmodel 同期リラクタンスモータ最適化の追加
    - [密度法による最適化](/docs/next/showcase/Dmodel/gradient_density)
    - [レベルセット法による最適化](/docs/next/showcase/Dmodel/gradient_levelset)
- [IPM8P48S応力制約下最適化例](/docs/next/showcase/IPM8P48S/pto)
- [IPM8P48Sサロゲート利用例](/docs/next/showcase/IPM8P48S/surrogate)