---
sidebar_position: 1
---

# インストール手順
## 前提条件
- Python 3.11.x 環境およびパッケージ管理ツールpipが必要です。
- EMSOptimizerの形状最適化機能を有効化するには、EMSolution*のEMSOptimizer専用パッケージをインストールする必要があります。
- （任意）EMSOptimizerとeMotorSolution* APIを連携したい場合は、eMotorSolution APIをインストールします。

*EMSolutionおよびeMotorSolutionのインストールに関しては、公式の[製品ページ](https://www.ssil.co.jp/product/EMSolution/product/)をご覧ください。

## インストール手順
1. 本リポジトリの"Releases"からEMSOptimizer最新バージョンのzip(or tar.gz)ファイル、および付随するwhlファイルをダウンロードします。

2. ダウンロードしたzipファイルをPCの任意の場所に展開します。

3. コマンドラインから、ダウンロードしたwhlファイルを`pip install`します。
```sh
pip install emsopt_engine-(version)-(environment)-(os).whl
```
※依存パッケージを同時にインストールするため、実行完了まで数分かかる場合があります。

### 開発者向け
zip(or tar.gz)ファイルをダウンロードおよび展開する代わりに、本リポジトリのソースコードをPCにクローンすることもできます。  
その場合でも3.の手順は必要です。