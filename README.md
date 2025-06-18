# MCWJA pywikibot
[Minecraft Wiki 日本語版](https://ja.mc.wiki/)向けに私（[Müller857](https://ja.mc.wiki/w/User:Müller857)）が使用している Pywikibot の `userscripts` です。

当面は[私のボット](https://ja.mc.wiki/User:BotM857)が作業を実行できるはずですが、このボットによる作業を前提とした方針などが立てられるようになったため、将来の編集者のためにソースを残しておきます。必要な時が来たら自由に使用・改変してください。
## 使用方法
Pywikibotの環境を整えた上で、ファイルを`pywikibot/scripts/userscripts`にダウンロードしてください。

大した代物ではないのでしばらくの間は適当な最新環境で動くと思いますが、開発時の環境は
* Python: 3.10.12
* Pywikibot: 9.6.3
です。

## スクリプト概要
詳細は各スクリプトの`-help`を参照してください。
|スクリプト名|用途|オプション|
|:-:|:-|:-|
|`tr_replace`|[テンプレート:Translate](https://ja.mc.wiki/w/Template:Translate)を最終翻訳で置換します。|なし|
|`tr_title`|[テンプレート:Translate title](https://ja.mc.wiki/w/Template:Translate_title)を呼んでいるページを翻訳後の名前に移動し、テンプレートを剥がし、関連するリダイレクト先を修正します。|なし|
|upcoming|完全版ができたものから追加予定|-|
