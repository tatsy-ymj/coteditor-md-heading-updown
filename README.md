# CotEditor Markdown Heading Up/Down

CotEditorで選択行のMarkdown見出しレベルを上下するAppleScriptです。

## Scripts

- `md_heading_up.applescript`: 選択行の見出しレベルを1つ上げます。
- `md_heading_down.applescript`: 選択行の見出しレベルを1つ下げます。

## Gists

- `md_heading_up.applescript`: https://gist.github.com/tatsy-ymj/4a0c57a3e2b36fa400d28a128dbb8378
- `md_heading_down.applescript`: https://gist.github.com/tatsy-ymj/a3264c8aa5820a0bedc3c4713c2f14e8

## Check

```sh
osacompile -o /tmp/md_heading_up.scpt md_heading_up.applescript
osacompile -o /tmp/md_heading_down.scpt md_heading_down.applescript
python3 tests/check_persistence.py
```

macOSとCotEditorが必要です。テストはCotEditorの辞書で実ソースをコンパイルした後、アプリとの入出力だけを合成データに置き換えて実行します。開いている文書は操作しません。

## 実行状態の保存防止

AppleScriptの暗黙の`run`で設定した変数は、コンパイル済みスクリプトの状態として保存されることがあります。選択文字列や位置を残さないため、上下両方のスクリプトで明示的な`on run`と`local`宣言を使用しています。今後、一時変数を追加する場合も`local`を宣言してください。

2026-10-05: 通常コンパイルと実行専用（`-x`）の双方で、長短の日本語・絵文字入り合成入力を別プロセスから繰り返し実行し、見出し変換結果と`.scpt`のバイト一致を確認しました。`local`宣言を除いた対照では選択文字列が保存されることも確認しています。これは合成入出力による検証であり、CotEditorのScriptsメニュー経由の動作・Undoは今回未検証です。

このMacの設置先は`~/Library/Application Scripts/com.coteditor.CotEditor/markdown/`です。`md_heading_up.^@j.applescript`と`md_heading_down.^@k.applescript`に対応するソースを配置します。Gistの更新はGitのpushとは別操作です。

## Publish

```sh
./publish_gists.sh
```

`gh` CLIでログイン済みであることが前提です。
