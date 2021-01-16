from django.contrib.auth import get_user, get_user_model
from django.core import mail
from django.test import TestCase
from django.urls import reverse
from accounts.forms import CustomSignupForm, CustomLoginForm, CustomResetPasswordForm, CustomResetPasswordKeyForm

from accounts.models import CustomUser

import re


class TestSignUp(TestCase):
    # テスト用ユーザーをself.test_userへ格納
    def setUp(self):
        self.test_user = {
            "email": "testuser001@example.com",
            "password1": "abcdefg123456",
            "password2": "abcdefg123456",
        }

    # サインアップページのロードが成功するか
    def test_for_signup_page_loads_successfully(self):
        response = self.client.get(reverse('account_signup'))

        self.assertEqual(response.status_code, 200)  # ステータスコードが200かどうか
        self.assertTemplateUsed(response, 'account/signup.html')  # 使用テンプレートが"account/signup.html"かどうか
        self.assertContains(response, 'csrfmiddlewaretoken')  # "account/signup.html"に動的に生成される"csrfmiddlewaretoken"が含まれるか
        self.assertIsInstance(  # "response.context['form']"が"SignupForm"のインスタンスかどうか
            response.context['form'], CustomSignupForm
        )

    # サインアップが成功することをテスト
    def test_for_successful_register(self):
        test_user_for_successful_register = self.test_user
        response = self.client.post(
            reverse('account_signup'),  # サインアップページのurlを取得し、self.client.postへわたす
            test_user_for_successful_register
        )

        # email, password1, password2をpost後リダイレクトされたか
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(
            response,
            '/accounts/confirm-email/',
            status_code=302,
            target_status_code=200,
            fetch_redirect_response=True
        )

        # 新規ユーザーが追加されたか
        self.assertTrue(
            CustomUser.objects.filter(
                email=self.test_user['email']
            ).exists()
        )

        # メールが送信されたか（厳密にはメールがoutboxに保存されたか）
        self.email = mail.outbox[0]
        self.assertEqual('testuser001@example.com', self.email.to[0])  # 宛先メールアドレスが正しいかどうか
        self.assertEqual('ユーザー登録確認メール', self.email.subject)  # 件名が正しいかどうか

        email_confirmation_message = 'ご登録ありがとうございます。\nまだ、登録は完了しておりません。\n登録を続けるには、以下リンクをクリックしてください。'
        self.assertIn(email_confirmation_message, self.email.body)  # メール本文にemail_confirmation_messageが含まれるか

        # 非ログイン状態かどうか
        self.assertTrue(
            get_user(self.client).is_anonymous
        )


class TestLogin(TestCase):

    # テスト用ユーザーをself.test_userへ格納
    def setUp(self):
        self.test_user = {
            "username": "testuser002",
            "email": "testuser002@example.com",
            "password": "abcdefg123456",
        }

    # ログインページのロードが成功するか
    def test_for_login_page_loads_successfully(self):

        response = self.client.get(reverse('account_login'))

        self.assertEqual(response.status_code, 200)  # ステータスコードが200かどうか
        self.assertTemplateUsed(response, 'account/login.html')   # 使用テンプレートが"account/login.html"かどうか
        self.assertContains(response, 'ログイン状態を維持する')  # "account/login.html"に動的に生成される"ログイン状態を維持する"が含まれるか
        self.assertContains(response, 'csrfmiddlewaretoken')  # "account/login.html"に動的に生成される"csrfmiddlewaretoken"が含まれるか
        self.assertIsInstance(  # "response.context['form']"が"LoginForm"のインスタンスかどうか
            response.context['form'], CustomLoginForm
        )

    # ログインが成功するかどうか
    def test_for_successful_login(self):
        # テスト用ユーザー作成
        get_user_model().objects.create_user(
            self.test_user['username'],
            self.test_user['email'],
            self.test_user['password']
        )

        # ポストするメールアドレスとパスワードをpost_dataに格納
        post_data = {
            'email': self.test_user['email'],
            'password': self.test_user['password']
        }

        # 新規ユーザが追加されたか
        self.assertTrue(
            CustomUser.objects.filter(
                email=self.test_user['email']
            ).exists()
        )

        # ログイン
        self.client.login(email=self.test_user['email'], password=self.test_user['password'])

        response = self.client.post(
            reverse("account_login"),
            post_data
        )

        # ログイン状態かどうか
        self.assertTrue(
            get_user(self.client).is_authenticated
        )

        # /index/へリダイレクトされたか
        self.assertRedirects(
            response,
            '/index/',
            status_code=302,
            target_status_code=200,
            fetch_redirect_response=True
        )


class TestLogout(TestCase):

    # テスト用ユーザーをself.test_userへ格納
    def setUp(self):
        self.test_user = {
            "username": "testuser003",
            "email": "testuser003@example.com",
            "password": "abcdefg123456",
        }

        # テスト用ユーザー作成
        get_user_model().objects.create_user(
            self.test_user['username'],
            self.test_user['email'],
            self.test_user['password']
        )

    def test_for_successful_logout(self):

        # ログイン
        status = self.client.login(email=self.test_user['email'], password=self.test_user['password'])
        self.assertEqual(status, True)

        # ログイン状態かどうか
        self.assertTrue(
            get_user(self.client).is_authenticated
        )

        self.client.logout()

        # 非ログイン状態かどうか
        self.assertTrue(
            get_user(self.client).is_anonymous
        )


class TestPasswordReset(TestCase):
    # テスト用ユーザーをself.test_userへ格納
    def setUp(self):
        self.test_user = {
            "username": "testuser004",
            "email": "testuser004@example.com",
            "password": "abcdefg123456",
        }

        # テスト用ユーザー作成
        get_user_model().objects.create_user(
            self.test_user['username'],
            self.test_user['email'],
            self.test_user['password']
        )

        # 新規ユーザが追加されたか
        self.assertTrue(
            CustomUser.objects.filter(
                email=self.test_user['email']
            ).exists()
        )

    # パスワードリセットページのロードが成功するか
    def test_for_password_reset_page_loads_successfully(self):
        response = self.client.get('/accounts/password/reset/')

        self.assertEqual(response.status_code, 200)  # ステータスコードが200かどうか
        self.assertTemplateUsed(response, 'account/password_reset.html')  # 使用テンプレートが"account/password_reset.html"かどうか
        self.assertContains(response, 'パスワード再設定用のメールを送信します')  # "account/login.html"に動的に生成される"ログイン状態を維持する"が含まれるか
        self.assertContains(response, 'csrfmiddlewaretoken')  # "account/password_reset.html"に動的に生成される"csrfmiddlewaretoken"が含まれるか
        self.assertIsInstance(  # "response.context['form']"が"ResetPasswordForm"のインスタンスかどうか
            response.context['form'], CustomResetPasswordForm

        )

    # ログインが成功するかどうか
    def test_for_post_password_reset(self):

        # ポストするメールアドレスとパスワードをpost_dataに格納
        post_data = {
            'email': self.test_user['email'],
            'password': self.test_user['password']
        }

        # account_reset_passwordへpost_dataをポストし、responseオブジェクトを受け取る
        response = self.client.post(
            reverse('account_reset_password'),
            post_data
        )

        # /accounts/password/reset/done/へリダイレクトされたか
        self.assertRedirects(
            response,
            '/accounts/password/reset/done/',
            status_code=302,
            target_status_code=200,
            fetch_redirect_response=True
        )

        # メールが送信されたか（厳密にはメールがoutboxに保存されたか）
        self.email = mail.outbox[0]
        self.assertEqual('testuser004@example.com', self.email.to[0])  # 宛先メールアドレスが正しいかどうか
        self.assertEqual('パスワードリセット', self.email.subject)  # 件名が正しいかどうか

        email_confirmation_message = 'パスワードリセットが申請されました。\n記載されているリンクからパスワードの再設定を行ってください。'
        self.assertIn(email_confirmation_message, self.email.body)  # メール本文にemail_confirmation_messageが含まれるか

        password_reset_url = re.search('http://.*/accounts/password/reset/key/.*/$', self.email.body).group()

        # パスワードリセットページのロードが成功するか
        response = self.client.get(password_reset_url)

        # "testuser004@example.com"のプライマリーキーを取得
        pk = CustomUser.objects.get(
                email=self.test_user['email']
            ).pk

        # リダイレクト先を変数へ代入
        password_reset_redirect_url = '/accounts/password/reset/key/' + str(pk) + '-set-password/'

        # '/accounts/password/reset/key/' + str(pk) + '-set-password/'へリダイレクトされたか
        self.assertRedirects(
            response,
            password_reset_redirect_url,
            status_code=302,
            target_status_code=200,
            fetch_redirect_response=True
        )

        # ポストする更新用パスワード
        post_data_for_reset_password = {
            'password1': 'hijklmn7890',
            'password2': 'hijklmn7890'
        }

        # password_reset_redirect_urlへpost_dataをポストし、responseオブジェクトを受け取る
        response = self.client.post(
            password_reset_redirect_url,
            post_data_for_reset_password
        )

        # /accounts/password/reset/key/done/へリダイレクトされたか
        self.assertRedirects(
            response,
            '/accounts/password/reset/key/done/',
            status_code=302,
            target_status_code=200,
            fetch_redirect_response=True
        )

        # パスワード更新後のユーザデータ
        post_data_for_reseted_password = {
            'email': self.test_user['email'],
            'password': 'hijklmn7890'
        }

        # ログイン
        status = self.client.login(email=self.test_user['email'], password='hijklmn7890')
        self.assertEqual(status, True)

        # 更新パスワード'hijklmn7890'でログインできるか
        response = self.client.post(
            reverse("account_login"),
            post_data_for_reseted_password
        )

        # ログイン状態かどうか
        self.assertTrue(
            get_user(self.client).is_authenticated
        )

        # /index/へリダイレクトされたか
        self.assertRedirects(
            response,
            '/index/',
            status_code=302,
            target_status_code=200,
            fetch_redirect_response=True
        )
