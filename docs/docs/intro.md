---
sidebar_position: 1
---

# インストール
## 前提条件
- Python 3.11.x 環境およびパッケージ管理ツールpipが必要です。
- EMSOptimizerの形状最適化機能を有効化するには以下の2点が必要です。
    - EMSolution(pyemsol)*のEMSOptimizer専用パッケージ
    - EMSOptimizerライセンスファイル（無償版／有償版）*
- （任意）EMSOptimizerとeMotorSolution* APIを連携するには、eMotorSolution APIをインストールします。

*必要パッケージおよびライセンスの入手については公式の[製品ページ](https://www.ssil.co.jp/product/EMSolution/product/)をご覧ください。

## インストール手順
1. Github [EMSOptimizerリポジトリ](https://github.com/EMSolution-SSIL/EMSOptimizer)の"Releases"から以下の2点をダウンロードします。
    1. EMSOptimizer最新バージョンのzipまたはtar.gzファイル
    2. i.に付随するwhlファイル（emsopt_engine）

2. ダウンロードしたzipまたはtar.gzファイルをPCの任意の場所に展開します。

3. ダウンロードしたwhlファイルをコマンドラインから`pip install`します。
```sh
pip install emsopt_engine-(version)-(environment)-(os).whl
```
※依存パッケージを同時にインストールするため、実行完了まで数分かかる場合があります。

### 開発者向け
zipまたはtar.gzファイルをダウンロード・展開する代わりに、リポジトリをPCにクローンすることもできます。  
その場合も3.の手順は実施する必要があります。