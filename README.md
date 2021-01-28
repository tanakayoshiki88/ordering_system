# ordering_system

## Requirements

1. python3
2. django
3. pillow
4. django-allauth
5. postgresql
6. psycopg2-binary


## Installation

1. $ brew install python

2. $ python3 --version

3. $ cd "any directory"
4. $ git clone https://github.com/tanakayoshiki88/ordering_system.git

5. $ cd ordering_system 

6. $ python3 -m venv venv

7. $ source venv/bin/activate

8. (venv) $ pip install django

9. (venv) $ python -m django --version

10. $ brew install postgresql
    1.  $ psql --version
    2.  $ brew services start postgresql
    3.  $ createdb -U "username" ordering_system
    4.  $ psql -lU "username"
    5.  (venv) $ pip install psyc opg2-binary
    6.  (venv) $ pip freeze
    7.  (venv) $ brew services stop postgresql
    8.  $ vi ~/.bash_profile
        ######*-- insert --*
        ```
        export DB_USER="your_username"
        export DB_PASSWORD="your_password"
        ```
    9.  $ source ~/.bash_profile
   
11. $ brew services start postgresql
   
12. (venv) $ pip install django-allauth

    (venv) $ pip freeze

13. (venv) $ pip install pillow

    (venv) $ pip freeze

14. $ cd config

    $ touch local_settings.py

    $ python get_secret_key.py > local_settings.py
    
    $ vi get_secret_key.py
    
    >   SECRET_KEY='*secret_key*'
    
    *vi command mode*
    ```
    :q!
    ```
    
    $ cd ..
    
15. (venv) $ python manage.py makemigrations --settings config.settings_dev

    (venv) $ python manage.py migrate --settings config.settings_dev
    
16. (venv) $ pyton manage.py createsuperuser --settings config.settings_dev

    >    Username (leave blank to use 'user1'): *"admin"*
    >
    >    Email address: *"your email address""*
    >
    >    Password: *"password"*
    >
    >    Password (again): *"again"* 
    >
    >    Superuser created successfully.
    
17. (venv) $ python manage.py runserver --settings config.settings_dev

    http://127.0.0.1:8000/

18. sidebar > Pages > Sign up

    input: email & password > "Register Account"
      
    terminal:
    > ご登録ありがとうございます。
    >
    > 登録を続けるには、以下リンクをクリックしてください。
    >
    > http://127.0.0.1:8000/accounts/confirm-email/XXXXXXXXXXXXXXXXXXXXXXXXXXXXXX/
    >
    
    Copy the url and paste it into your browser.
    
    Then press the "confirm" button.
    
19. http://127.0.0.1:8000/admin

    username: admin
    
    password: *"admin password"*
