---
sidebar_position: 1
---

# インストールガイド
## ソフトウェア構成
- Github [EMSOptimizerリポジトリ](https://github.com/EMSolution-SSIL/EMSOptimizer)から入手するもの
    - EMSOptFree: 公開ソースコード部です。基本的な数理最適化機能を提供します。
    - EMSOptEngine: リポジトリ"Releases"からwhl形式でダウンロード可能なpythonモジュールです。EMSOptFreeを動作させるためには本モジュールのインストールが必要です。
- SSIL公式から入手するもの*→形状最適化機能を有効化するために必要です。
    - EMSOptAnalyzer: 形状最適化における形状定義および解析を行うpythonモジュールです。
    - pyemsol: 電磁界シミュレータエンジンEMSolutionのpython版パッケージです。
    - ライセンス認証
    - （任意）eMotorSolution API: eMotorSolutionのpython APIです。eMotorSolutionとEMSOptimizerを連携させたい場合にインストールします。連携機能については[発展的なトピック > eMotorSolutionとの連携](./advanced/link_ems.md)をご覧ください。

*詳しくは公式の[製品ページ](https://www.ssil.co.jp/product/EMSolution/product/)をご覧ください。なお、これらのモジュール等が無い場合もベンチマーク関数による最適化アルゴリズムのテスト機能などは使用可能です。

## インストール手順
*Python 3.11.x 環境およびパッケージ管理ツールpipが必要です。

1. Github [EMSOptimizerリポジトリ](https://github.com/EMSolution-SSIL/EMSOptimizer)の"Releases"から以下の2点をダウンロードします。
    1. EMSOptFree最新バージョンのzipまたはtar.gzファイル
    2. i.に付随するwhlファイル（emsopt_engine）

2. ダウンロードしたzipまたはtar.gzファイルをPCの任意の場所に展開します。

3. ダウンロードしたwhlファイルをコマンドラインから`pip install`します。
```sh
pip install emsopt_engine-(version)-(environment)-(os).whl
```
※依存パッケージを同時にインストールするため、実行完了まで数分かかる場合があります。

4. 形状最適化機能を有効化する場合、必要モジュール等をそれぞれの手順に従ってインストールします。

### 開発者向け
zipまたはtar.gzファイルをダウンロード・展開する代わりに、リポジトリをPCにクローンすることもできます。