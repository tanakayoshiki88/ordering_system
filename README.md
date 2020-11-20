# ordering_system

## Requirement

python3
django
pillow
django-allauth
postgresql
psycopg2-binary


## Installation

1. $ brew install python

   $ python3 --version

2. $ cd "any directory"
   $ git clone https://github.com/tanakayoshiki88/ordering_system.git

3. $ cd ordering_system 

4. $ python3 -m venv venv

5. $ source venv/bin/activate

6. (venv) $ pip install django
   (venv) $ python -m django --version
   (venv) $ python manage.py createsuperuser --settings config.settings_dev

7. $ brew install postgresql
   $ psql --version
   $ brew services start postgresql
   $ createdb ordering_system
   $ psql -l
   (venv) $ pip install psycopg2-binary
   (venv) $ pip freeze
   (venv) $ brew services stop postgresql
   $ vi ~/.bash_profile
     -- insert --
     export PATH=$PATH:/"your_install_path"/ordering_system
     export DB_USER="your_username"
     export DB_PASSWORD="your_password"
   $ source ~/.bash_profile
   $ brew services start postgresql
   
8. (venv) $ pip install django-allauth
   (venv) $ pip freeze

9. (venv) $ pip install pillow
   (venv) $ pip freeze

10. (venv) $ pip install django-allauth
    (venv) $ pip freeze

11. $ cd config
    $ touch local_settings.py
    $ python get_secret_key.py > local_settings.py

11. (venv) $ python manage.py makemigrations --settings config.settings_dev
    (venv) $ python manage.py migrate --settings config.settings_dev

12. (venv) $ python manage.py runserver --settings config.settings_dev
    http://127.0.0.1:8000/

13. sidebar > Pages > Sign up

    input: email, password > "Register Account"
      
    terminal:
    > ご登録ありがとうございます。
    > 登録を続けるには、以下リンクをクリックしてください。
    > http://127.0.0.1:8000/accounts/confirm-email/Mw:1kebu9:LseFfUAYjaSoBbcW0lo8s6B_BC6AaO_bMkXxXOi2UcE/
    > -------------------------------------------------------------------------------
    
    Copy the url and paste it into your browser.
    Then press the "confirm" button.



   
