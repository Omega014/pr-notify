# pr-notify

GithubのPR状況を取得してSlackに通知するBot

# How To Use

## setting
1. configに書かれた必要な環境変数を各々の場所に設定しておく
2. cronかなにかでmain.pyが自動で実行されるように設定する
   - Ex) 0 6 * * 1-5 python3 /home/ubuntu/pr-notify/main.py
3. Githubのlabelに `review request` と `reviewed` を追加する

## After
PRを作成したら `review request` を付けてください.
定刻になると (cron等を仕込んでいる場合) scriptがレビュー依頼のあるPRを自動で引っ張ってきて指定のSlack channelに情報を流します.
`reviewed` も同様, このlabelがつけられている場合はレビュー済みのPRとして情報が流れます.
