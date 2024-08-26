<p style="display: inline">
<img src="https://img.shields.io/badge/-Python-3776AB.svg?logo=python&style=plastic">
<img src="https://img.shields.io/badge/-Django-092E20.svg?logo=django&style=plastic">
</p>
# two-fa-django
Djangoで2FA(TOTP)で実装しただけです。

[document](https://qiita.com/hsano43/items/509544025882f852aa62)
に対して、説明用のコードとして作成しました

# Requirement
* Python 3.12 以上
* Django 5.1.0以上
* PyJWT　2.9.0以上
* qrcode 7.4.2以上
* pyotp  2.9.0以上

# Installation
Pythonがない環境なら事前にインストールしてください
後は、上記のRequirementを順にインストールしてください
```bash
pip install Django==5.1.0 pyjwt qrcode pyotp
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
表示されるQRコードをGoogle Authenicatorで撮影し、表示されるコードを入力することでユーザー登録およびログインが完了します。


