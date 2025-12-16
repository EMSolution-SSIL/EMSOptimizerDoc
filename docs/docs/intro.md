---
sidebar_position: 1
---

# インストールガイド
## ソフトウェア構成
EMSOptimizerは以下の2点から構成されます。

1. Github [EMSOptimizerリポジトリ](https://github.com/EMSolution-SSIL/EMSOptimizer)から入手するもの
    - EMSOptFree
        - 公開ソースコード部です。基本的な数理最適化機能を提供します。
    - EMSOptEngine
        - リポジトリ内"Releases"からwhl形式でダウンロード可能なpythonモジュールです。EMSOptFreeを動作させるためには本モジュールのインストールが必要です。
2. SSIL公式から個別に提供されるもの*→**形状最適化機能を有効化するために必要です**。
    - EMSOptAnalyzer
        - 形状最適化における形状定義および解析を行うpythonモジュールです。
    - pyemsol
        - 電磁界シミュレータエンジンEMSolutionのpython版パッケージです。EMSOptAnalyzerを駆動させるために必要です。
    - ライセンス認証情報（ライセンスファイルまたはCodeMeterライセンスキー）**
    - （任意）eMotorSolution API
        - eMotorSolutionのpython APIです。eMotorSolutionとEMSOptimizerを連携させたい場合にインストールします。連携機能については[発展的なトピック > eMotorSolutionとの連携](./advanced/link_ems.md)をご覧ください。

*詳しくは公式の[製品ページ](https://www.ssil.co.jp/product/EMSolution/product/)をご覧ください。なお、1.単独でもベンチマーク関数による最適化アルゴリズムのテストなど、形状最適化を除いた一部機能は使用可能です。

**個別提供のモジュール群はプロテクトされており、利用にはライセンス認証が必要です。以下の2種類のプロテクト方式のいずれかを選択します。
- ライセンスファイルプロテクト：独自のライセンスファイルを使用したプロテクト方式です。
- CodeMeterプロテクト：ライセンスプロテクションソフトウェアCodeMeterを使用したプロテクト方式です。
:::info
**以下の機能を利用するにはCodeMeterプロテクトが必須です**。
- eMotorSolution連携機能
- 計算ノード間分散処理機能
:::

## インストール手順
*Python 3.11.x 環境およびパッケージ管理ツールpipが必要です。

1. Github [EMSOptimizerリポジトリ](https://github.com/EMSolution-SSIL/EMSOptimizer)の"Releases"から以下をダウンロードします。
    1. EMSOptFree最新バージョンのzipまたはtar.gzファイル
    2. EMSOptFreeに付随するwhlファイル（emsopt_engine）

2. ダウンロードしたzipまたはtar.gzファイルをPCの任意の場所に展開します。
:::info 開発者向け
zipまたはtar.gzファイルをダウンロード・展開する代わりに、リポジトリをPCにクローンすることもできます。
:::

3. ダウンロードしたwhlファイルをコマンドラインから`pip install`します。
```sh
pip install emsopt_engine-(version)-(environment)-(os).whl
```
※依存パッケージを同時にインストールするため、実行完了まで数分かかる場合があります。

4. 形状最適化機能を有効化するには、SSILから提供される必要モジュール等をそれぞれの手順に従ってインストールします。  
- （ライセンスファイルプロテクト時）ライセンスファイルは以下のデフォルトのフォルダに配置します。
    - Windows: `C:\ProgramData\SSIL\EMSolution\`
    - Linux: `/usr/local/emsol/`
- （CodeMeterプロテクト時）以下の追加手順を実施します。ライセンスキーは追加手順内にて使用します。

### CodeMeterプロテクト時の追加手順
#### CodeMeter Runtimeのインストール
1. CodeMeter Runtimeダウンロードページにアクセスします：https://www.wibu.com/us/products/codemeter/runtime.html
2. ご使用のOS（Windows、macOS、Linux）に対応したバージョンをダウンロードします。
3. Webサイト上の指示に従って、CodeMeter Runtimeをインストールします。
4. インストール完了後、コンピューターを再起動します。

#### ライセンスのアクティベーション
1. SSILから提供されるアクティベーションページのURLをブラウザで開きます。
2. アクティベーションページの指示に従い、ライセンスをアクティベートします。
3. アクティベーション後，CodeMeter Control Centerを開き，ライセンスが正しく登録されていることを確認します。
