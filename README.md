# mock_mailman

Djangoの学習用に、[Mailman](https://www.list.org/)の一部機能を実装したものになります。

# 環境構築

[rye](https://rye-up.com/guide/basics/) をセットアップする

サーバーの起動

`rye run python3.12 ./src/manage.py runserver`

簡易的なSMTPサーバーの起動

`rye run python3.12 -m aiosmtpd -n -l localhost:8025`
