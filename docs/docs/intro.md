---
sidebar_position: 1
---

# インストールガイド
## ソフトウェア構成
**EMSOptimizerは以下の3点（以下、EMSOptimizerパッケージ群）から構成されます**。
- EMSOptFree
    - 公開ソースコード部です。EMSOptimizerのCLIコマンドや最適化ループ、最適化アルゴリズムの実装例などを提供します。
- EMSOptEngine
    - EMSOptFree駆動用のpythonパッケージです。EMSOptFreeを動作させるためには本パッケージのインストールが必要です。
- EMSOptAnalyzer
    - 形状最適化における形状定義および解析を行うpythonパッケージです。形状最適化を行う場合は上記2点に加えてインストールが必要です。

また、**EMSOptimizerの形状最適化機能を動作させるには以下の関連パッケージ群が必要です\***。
- pyemsol
    - 電磁界シミュレータエンジンEMSolutionのpython版パッケージです。EMSOptAnalyzerを駆動させるために必要です。
:::info
EMSOptAnalyzerの駆動には専用のpyemsolが必要です。これはEMSOptAnalyzer提供時に一緒に提供されます。
:::
- （任意）eMotorSolution API
    - eMotorSolutionのpython APIです。eMotorSolutionとEMSOptimizerを連携させたい場合にインストールします。連携機能については[発展的なトピック > eMotorSolutionとの連携](./advanced/link_ems.md)をご覧ください。
- ライセンス認証情報（ライセンスファイルまたはCodeMeterライセンスキー）**

*形状最適化用の関連パッケージ群が無い状態でも、形状最適化を除いた一部機能（ベンチマーク関数による最適化アルゴリズムのテストなど）は利用可能です。

**EMSOptimizerパッケージ群の一部および関連パッケージ群はライセンスプロテクトされており、利用にはライセンス認証が必要です。以下の2種類のプロテクト方式のいずれかを選択します。
- ライセンスファイルプロテクト：独自のライセンスファイルを使用したプロテクト方式です。
- CodeMeterプロテクト：ライセンスプロテクションソフトウェアCodeMeterを使用したプロテクト方式です。
:::info
**以下の機能はCodeMeterプロテクト時のみ利用可能です**。
- [eMotorSolution連携機能](./advanced/link_ems.md)
- [計算ノード間分散処理機能](./advanced/distribution.md)
:::

## インストール手順
*Python 3.11.x (xは任意のマイナーバージョン) 環境およびパッケージ管理ツールpipが必要です。

1. EMSOptimierパッケージ群をインストールします。
- EMSOptFreeは圧縮フォルダ（`EMSOptimizer`）として提供されます。ご使用の環境にて解凍のうえ、任意の場所にフォルダごと配置してください。
- EMSOptEngine, EMSOptAnalyzerはwhlファイルとして提供されます。以下のコマンドによってインストールしてください。
```sh
pip install emsopt_engine-(version)-(environment)-(os).whl
pip install emsopt_analyzer-(version)-(environment)-(os).whl
```

2. SSILから提供される関連パッケージ群をそれぞれの手順に従ってインストールします。  
- （ライセンスファイルプロテクト時）ライセンスファイルは以下のデフォルトのフォルダに配置します。
    - Windows: `C:\ProgramData\SSIL\EMSolution\`
    - Linux: `/usr/local/emsol/`
- （CodeMeterプロテクト時）以下の追加手順を実施します。ライセンスキーは追加手順内にて使用します。

### CodeMeterプロテクト時の追加手順
#### CodeMeter User Softwareのインストール
1. CodeMeter User Softwareダウンロードページにアクセスします：https://www.wibu.com/support/user/user-software.html
2. ご使用のOS（Windows、macOS、Linux）に対応したCodeMeter User Runtimeをダウンロードします。
3. Webサイト上の指示に従って、CodeMeter User Runtimeをインストールします。
4. **Linux OSの場合のみ**、CodeMeter User SoftwareダウンロードページからAxProtector Runtime for Linuxをダウンロードします。
5. **Linux OSの場合のみ**、Webサイト上の指示に従って、AxProtector User Runtimeをインストールします。
6. インストール完了後、コンピューターを再起動します。

#### ライセンスのアクティベーション
1. SSILから提供されるアクティベーションページのURLをブラウザで開きます。
2. アクティベーションページの指示に従い、ライセンスをアクティベートします。
3. アクティベーション後，CodeMeter Control Centerを開き，ライセンスが正しく登録されていることを確認します。
