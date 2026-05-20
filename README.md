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
```

## Publish

```sh
./publish_gists.sh
```

`gh` CLIでログイン済みであることが前提です。
