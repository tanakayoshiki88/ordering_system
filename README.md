# ordering_system

## Requirements

1. python3
2. django
3. pillow
4. django-allauth
5. postgresql
6. psycopg2-binary

## Installation

1. $ brew install postgresql

   1. $ psql --version
   2. $ brew services start postgresql
   3. $ createdb -U "your_username" ordering_system
   4. $ psql -l
   5. $ vi ~/.bash_profile
      ```
      export DB_USER="your_username"
      ```
   6. $ source ~/.bash_profile

2. $ brew install python

3. $ python3 --version

4. $ cd "any directory"

5. https://github.com/tanakayoshiki88/ordering_system.git から zipファイルを任意のディレクトリにダウンロードしてください

6. zipファイルをダウンロードした任意のディレクトリに cdコマンドで移動して、zipファイルを解凍してください

7. $ python3 -m venv venv

8. $ source venv/bin/activate

9. (venv) $ pip install -r requirements.txt

10. $ (venv) cd config

    $ (venv) python3 get_secret_key.py > local_settings.py

    $ (venv) cat local_settings.py

    > SECRET*KEY='\_secret_key*'

    $ (venv) cd ..

11. (venv) $ python3 manage.py migrate --settings config.settings_dev
12. (venv) $ python3 manage.py createsuperuser --settings config.settings_dev

    > Username (leave blank to use 'user1'): _"admin"_
    >
    > Email address: _"your email address""_
    >
    > Password: _"password"_
    >
    > Password (again): _"again"_
    >
    > Superuser created successfully.

13. (venv) $ python3 manage.py runserver --settings config.settings_dev

    http://127.0.0.1:8000/

14. sidebar > Pages > Sign up

    input: email & password > "Register Account"

    terminal:

    > ご登録ありがとうございます。
    >
    > 登録を続けるには、以下リンクをクリックしてください。
    >
    > http://127.0.0.1:8000/accounts/confirm-email/XXXXXXXXXXXXXXXXXXXXXXXXXXXXXX/

    URL をコピー&ペーストしてブラウザで表示し、"confirm"ボタンをクリックしてください。

15. http://127.0.0.1:8000/admin

    username: _"admin"_

    password: _"admin password"_
