---
name: emsoptimizer-docs-translator
description: EMSOptimizerのDocusaurusドキュメントを、日本語を正本として英語版へ翻訳・同期するためのスキル。`docs/` から `i18n/en/docusaurus-plugin-content-docs/current/` へのMarkdown/MDX英訳、`current.json`・`version-*.json` 等のDocusaurus JSON翻訳、既存英訳の差分更新、用語統一、コード・設定キー・リンク先の保持、英訳後の検証を行う。EMSOptimizerドキュメントの英訳、日英同期、翻訳漏れ確認、sidebar等のUIラベル翻訳、英語版更新を依頼されたときに使用する。
---

# EMSOptimizer ドキュメント英訳

日本語版を唯一の正本として扱い、英語版を追従させる。既存の英訳は可能な限り維持し、日本語で変更された箇所だけを更新する。

## 基本方針

- 作業前に `references/glossary.yml` を読む。
- 原文は原則 `docs/`、英語版は原則 `i18n/en/docusaurus-plugin-content-docs/current/` とする。
- ユーザーが別パスを指定した場合は指定を優先する。
- `versioned_docs/` と `i18n/en/docusaurus-plugin-content-docs/version-*` は、明示的に依頼されない限り変更しない。
- 日本語原文の意味を追加・削除・推測で補完しない。原文に曖昧さや誤りの疑いがある場合は、英訳で勝手に修正せず指摘する。
- 既存英訳がある場合、全文再翻訳を避ける。日本語側の変更箇所に対応する英語だけを更新する。
- 用語集にない重要な専門用語が複数ページで繰り返される場合、訳語を勝手に揺らさず、必要なら `references/glossary.yml` への追加候補として報告する。

## ワークフロー

1. リポジトリ構成を確認する。
   - `docs/`
   - `i18n/en/docusaurus-plugin-content-docs/current/`
   - `docusaurus.config.js` または `docusaurus.config.ts`
   - `package.json`
   - `i18n/en/docusaurus-plugin-content-docs/current.json` および既存の `version-*.json`
2. `references/glossary.yml` を読み、固定語・翻訳禁止語・注記を把握する。
3. 翻訳対象を決める。
   - 英語版が存在しない場合: `docs/` の `.md` / `.mdx` を初回翻訳する。
   - 英語版が存在する場合: ユーザー指定のファイル、Git差分、未翻訳ファイルを優先する。
   - Git差分を使う場合は、原文側で変更されたファイルだけを対象にし、無関係な英語ファイルを書き換えない。
4. Markdown/MDXを英訳する。
5. Docusaurus JSON翻訳ファイルを更新する。sidebarやplugin設定が変更されている場合は、リポジトリの既存コマンドに従って `write-translations` を実行し、新規キーを抽出してから英訳する。
6. `scripts/validate_translation.py` を実行して構造保持とJSON翻訳漏れを確認する。
7. リポジトリに利用可能なDocusaurus buildコマンドがある場合、英語localeをビルドして確認する。
8. 変更ファイル、検証結果、未解決点を短く報告する。

## 翻訳ルール

### Front matter

- `title`、`description`、`sidebar_label` など、ユーザーに表示される文章は英訳する。
- `id`、`slug`、`sidebar_position`、`pagination_next`、`pagination_prev`、`custom_edit_url` など、識別・ルーティング・並び順に関わる値は原則維持する。
- キー名自体は変更しない。

### Markdown / MDX

- 見出し、本文、表、リスト、注記本文、画像alt、リンク表示テキストを英訳する。
- Markdown/MDXの階層、見出しレベル、リスト構造、表構造を維持する。
- リンク先URL・相対パスを変更しない。表示テキストだけ英訳する。
- 画像パスを変更しない。
- `:::note`、`:::tip`、`:::warning` などのadmonition種別を変更しない。
- MDXコンポーネント名、属性名、式、import/exportは変更しない。表示用文字列だけが明確に文章である場合に限って英訳する。

### Docusaurus JSON翻訳

`i18n/en/docusaurus-plugin-content-docs/current.json` と `version-*.json` も翻訳対象として扱う。これらはsidebar categoryなど、Markdown外に定義されたdocsプラグインの表示文字列を翻訳するためのファイルである。

- JSON翻訳ファイルが未生成、またはsidebar/plugin設定に変更がある場合は、リポジトリのpackage managerに合わせてDocusaurusの `write-translations --locale en` を実行する。npmの場合の例は `npm run write-translations -- --locale en`。
- 既存翻訳を保持したまま新規キーを追加する通常実行を優先する。`--override` はユーザーが明示的に完全再生成を求めた場合だけ使用する。
- 各エントリでは **`message` の値だけを英訳**する。JSONオブジェクトのキーは変更しない。
- `description` はDocusaurusが翻訳対象の意味を示すメタ情報なので、原則変更しない。
- キーや `description` に日本語が残っていても、それだけを理由に翻訳漏れと判断しない。
- `message` に `{name}`、`{versionLabel}` などのプレースホルダが含まれる場合、名前・個数を完全に維持する。
- HTML/Markdown断片やコードリテラルが `message` に含まれる場合、構造や識別子を維持し、表示文言だけを英訳する。
- `current.json` は `docs/` / `current/` に対応する。`version-X.Y.Z.json` は対応するversioned docsのUI翻訳として扱い、過去版は明示的に依頼された場合だけ更新する。
- リリース時に英語版を固定する依頼では、本文の `current/` とあわせて、その時点の `current.json` が対応する `version-X.Y.Z.json` に反映されていることを確認する。

例:

```json
{
  "sidebar.docsSidebar.category.基本の使い方": {
    "message": "Getting Started",
    "description": "The label for category 基本の使い方 in sidebar docsSidebar"
  }
}
```

この例では、キーと `description` は維持し、`message` だけを英訳する。

### コード・設定・識別子

- fenced code blockの内容を変更しない。
- インラインコードを変更しない。
- CLIコマンド、CLIオプション、Python識別子、クラス名、関数名、設定キー、YAML/JSONキー、ファイル名、パスを変更しない。
- 製品名・アルゴリズム名・略語は `references/glossary.yml` に従う。

### 英文スタイル

- 製品ドキュメントとして簡潔で技術的に明瞭な英語にする。
- 日本語の語順を機械的に残さず、意味を保った自然な技術英語にする。
- 不必要に説明を追加しない。
- 同じ概念には同じ訳語を使う。
- 見出しは既存英語ドキュメントのスタイルがある場合はそれに合わせる。

## 差分更新

既存英訳がある場合は次を守る。

1. 変更された日本語部分を特定する。
2. 既存英訳の対応部分だけを編集する。
3. 原文で変更されていない段落を言い換えない。
4. ファイル移動・削除が日本語側で行われた場合は、英語側も対応させる。
5. 新規ページは同じ相対パスで英語版を作成する。

Git差分の基準が不明な場合は、勝手に大規模な再翻訳を行わず、未翻訳ファイルと現在の作業ツリー差分を優先する。

## 検証

翻訳後、スキル内の検証スクリプトを実行する。

```text
python <skill>/scripts/validate_translation.py --repo-root <repository-root>
```

特定ファイルだけ確認する場合は `--files` を使う。

```text
python <skill>/scripts/validate_translation.py --repo-root <repository-root> --files getting-started/Introduction.md guides/machine_config.md
```

JSON翻訳も明示的に確認する場合は `--json-files` を使う。

```text
python <skill>/scripts/validate_translation.py --repo-root <repository-root> --json-files current.json version-1.0.0.json
```

このスクリプトでは主に次を確認する。

- 英語版ファイルの欠落
- 保持対象front matter値の不一致
- fenced code blockの内容変更
- インラインコードの変更
- Markdownリンク先・画像パスの変更
- `current.json` 等で `message` が日本語のまま残っていないか
- JSON翻訳ファイルの構文と `message` の有無

スクリプトがエラーを報告した場合は、翻訳内容を修正して再実行する。

その後、リポジトリの既存スクリプトに合わせてDocusaurusの英語localeをビルドする。例えばnpm運用で `build` が定義されている場合は、英語localeだけのbuildを優先する。

## 完了報告

最後に次だけを簡潔に示す。

- 翻訳・更新したファイル
- 新規作成／削除した英語ファイル
- 用語集への追加候補
- 検証スクリプトとDocusaurus buildの結果
- 原文の曖昧さ等、ユーザー判断が必要な点

翻訳本文をチャットへ大量に再掲しない。
