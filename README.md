<p style="display: inline">
<img src="https://img.shields.io/badge/-Python-3776AB.svg?logo=python&style=plastic">
<img src="https://img.shields.io/badge/-Django-092E20.svg?logo=django&style=plastic">
</p>
# jwt_django
Djangoの認証(login/logout)機能にJWT(Json Web Token)を組み込んだだけです。
JWTの説明用の 

[document](https://qiita.com/hsano43/items/509544025882f852aa62)
に対して、説明用のコードとして作成しました

# Requirement
* Python 3.12 以上
* Django 5.0.4以上
* ToJWT　2.9.0以上

# Installation
Pythonがない環境なら事前にインストールしてください
後はDjangoとPyJWTをインストールするだけです
```bash
pip install Django==5.0.6 pyjwt
```

myapp/setting.py内で定義されているJWT_SECRET_KEYとSECRET_KEYの入力だけしてください。
JWT_SECRET_KEYはJWT内で利用する秘密鍵で、SECRET_KEYはDjangoの秘密鍵です。
予想されずにある程度長い文字列であればなんでもいいです。
```python
JWT_SECRET_KEY = ""
SECRET_KEY = ""
```

db.sqlite3は上げていないので事前にマイグレーションを実施してください
```bash
python manage.py makemigrations 
python manage.py migrate
```

# Usage

ルート上で次のコマンドを実行すればrunserverが立ち上がります。
```
python manage.py runserver
```

```http://localhost:8000/accounts/signup/```にアクセスしてユーザー登録し、
ログイン画面でログインすればセッションIDがJWTに変わっていることが確認できます。
