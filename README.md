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
   3. $ createdb -U "username" ordering_system
   4. $ psql -l
   5. $ brew services stop postgresql
   6. $ vi ~/.bash_profile
      ```
      export DB_USER="your_username"
      export DB_PASSWORD="your_password"
      ```
   7. $ source ~/.bash_profile

2. $ brew install python

3. $ python3 --version

4. $ cd "any directory"

5. $ git clone https://github.com/tanakayoshiki88/ordering_system.git

6. $ cd ordering_system

7. $ python3 -m venv venv

8. $ source venv/bin/activate

9. (venv) $ pip install -r requirements.txt

10. $ (venv) cd config

    $ (venv) python get_secret_key.py > local_settings.py

    $ (venv) cat get_secret_key.py

    > SECRET*KEY='\_secret_key*'

    $ (venv) cd ..

11. (venv) $ python manage.py migrate --settings config.settings_dev
12. (venv) $ pyton manage.py createsuperuser --settings config.settings_dev

    > Username (leave blank to use 'user1'): _"admin"_
    >
    > Email address: _"your email address""_
    >
    > Password: _"password"_
    >
    > Password (again): _"again"_
    >
    > Superuser created successfully.

13. (venv) $ python manage.py runserver --settings config.settings_dev

    http://127.0.0.1:8000/

14. sidebar > Pages > Sign up

    input: email & password > "Register Account"

    terminal:

    > ご登録ありがとうございます。
    >
    > 登録を続けるには、以下リンクをクリックしてください。
    >
    > http://127.0.0.1:8000/accounts/confirm-email/XXXXXXXXXXXXXXXXXXXXXXXXXXXXXX/

    Copy the url and paste it into your browser.

    Then press the "confirm" button.

15. http://127.0.0.1:8000/admin

    username: _"admin"_

    password: _"admin password"_
