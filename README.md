# クラウドワークス新規案件チェックスクリプト
## 準備（Windows、Mac共通）
### １．config.iniに必要項目を書き込んでください。
メールは自分から自分に送信します。<br>
[CW Category ID]の欄は、チェックしたい仕事カテゴリの数字を登録してください。<br>
何個でも登録可能です。<br>
例：「HTML・CSSコーディング」なら「16」、「ランディングページ（LP）制作」なら「17」等。<br>

### ２．Googleの設定で安全性の低いアプリのアクセスを許可してください。
（アカウント管理→セキュリティ）<br>

### ３．ChromeDriverを配置してください。
https://chromedriver.chromium.org/downloads から<br>
Chromeのバージョンに合ったChromeDriverをダウンロードして、同じディレクトリに配置してください。<br>
Windowsは「chromedriver.exe」、Macは「chromedriver」になります。<br>
<br>
※Chromeをインストールしていないと使えません。<br>
またChromedriverとChrome本体のバージョンが一致していないとエラーになります。<br>
もしエラーになったら両方を同じバージョンに合わせてください。<br>
<br>
初回起動時に「cw_job_log_category_XX.txt」というファイル（XXはカテゴリID）が生成され、新着メール通知が来ます。<br>
2回目以降は新着があった時だけメール通知します。<br>

## Windowsで自動化
### Windowsタスクスケジューラ（Windows管理ツール）に登録
１．「操作」→「タスクの作成」<br>
２．「全般」タブで名前を入力、「最上位の権限で実行する」にチェック<br>
３．「操作」タブで新規追加<br>
４．「プログラム/スクリプト」でcw_scraping_script.exeを指定<br>
５．「トリガー」タブで新規追加<br>
６．「設定」を「毎日」にして、「詳細設定」の「繰り返し間隔」にチェック<br>
７．「繰り返し間隔」はお好みで、「継続時間」を「1日」に<br>
８．「OK」を押して登録を完了<br>

## Macで自動化
### Pythonを導入してlaunchdに登録
１．Pythonのインストール
homebrew（https://brew.sh/index_ja ）を使ってPythonをインストールします。<br>
ターミナルで下記２つのコマンドを実行してください。<br>
（ターミナルはアプリケーションのユーティリティの中にあります。）<br>
$ /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"<br>
$ brew install python<br>

２．launchdの設定<br>
「~/Library/」にLaunchAgentsという名前のディレクトリを作成し、<br>
cw_scraping_script.plistを配置してください。<br>

cw_scraping_script.plistをエディタで開いて、"自分の環境に合わせて書き換えてください"と書かれた場所を変更します。<br>
cw_scraping_script.pyファイルを保存したディレクトリまでのパスを書いてください。<br>
パスはフォルダを右クリックしたあと「option」キーを押したらメニューに表示されます。<br>

<StartInterVal>の下の300という数字は更新間隔（秒）です。<br>
デフォルトは300秒（5分）置きなので、お好みに変更してください。<br>

設定が済んだら下記のコマンドを実行してください。<br>
$ launchctl load /Library/LaunchAgents/cw_scraping_script.plist<br>
<br>
停止するまで定時実行するようになります。<br>
停止する時は下記の通りです。<br>
$ launchctl unload /Library/LaunchAgents/cw_scraping_script.plist<br>

３．ダウンロードしたアプリケーションの実行許可<br>
ターミナルで下記のコマンドを実行してください。<br>
$ sudo spctl --master-disable<br>
<br>
Macのシステム環境設定からセキュリティとプライバシーを開きます。<br>
「ダウンロードしたアプリケーションの実行許可：」に「すべてのアプリケーションを許可」があるのでチェックを入れてください。<br>
