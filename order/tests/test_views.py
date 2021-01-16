from django.contrib.auth import get_user, get_user_model
from django.test import TestCase
from django.core import mail
from django.urls import reverse

from order.forms import ContactForm

from accounts.models import CustomUser
from order.models import Order
from item.models import Item
from cart.models import Cart, CartItem

import os


class TestIndexView(TestCase):

    """インデックスページ表示機能テスト"""
    def test_index_page_loads(self):

        # インデックスページを取得
        response = self.client.get(reverse("order:index"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "order/index.html")  # 使用テンプレートが"order/index.html"かどうか
        self.assertContains(response, "Juhatchu is ordering system")  # "order/index.html"に文字列："X - order is ordering system"が含まれているか


class TestContactView(TestCase):

    def setUp(self):

        # お問い合わせメール送信用データ
        self.post_data = {
            "last_name": "abcあいう氏123",
            "first_name": "abcあいう名123",
            "email": "test-contact-mail@example.com",
            "subject": "お問い合わせメール送信テスト",
            "message": "お問い合わせメール送信テスト"
        }

        # お問い合わせメール送信失敗用データ
        self.post_data_failure = {
            "last_name": "",
            "first_name": "abcあいう名123",
            "email": "test-contact-mail@example.com",
            "subject": "お問い合わせメール送信テスト",
            "message": "お問い合わせメール送信テスト"
        }

    """問い合わせ機能テスト"""
    # お問い合わせページ表示テスト
    def test_contact_page_loads(self):

        # お問い合わせページを取得
        response = self.client.get(reverse("order:contact"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "order/contact.html")  # 使用テンプレートが"order/index.html"かどうか
        self.assertContains(response, "Juhacchu | Contact US")  # "order/index.html"に文字列："X - order is ordering system"が含まれているか
        self.assertContains(response,
                            'csrfmiddlewaretoken')  # "account/contact.html"に動的に生成される"csrfmiddlewaretoken"が含まれるか
        self.assertIsInstance(  # "response.context['form']"が"ContactForm"のインスタンスかどうか
            response.context['form'], ContactForm
        )

    # お問い合わせメール送信テスト
    def test_contact_send_email(self):

        # ContactViewへpost_dataをポスト
        response = self.client.post(
            reverse("order:contact"),
            self.post_data,
            follow=True
        )

        # /index/へリダイレクトされたか
        self.assertRedirects(
            response,
            '/contact/',
            status_code=302,
            target_status_code=200,
            fetch_redirect_response=True
        )

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "order/contact.html")  # 使用テンプレートが"order/icontact.html"かどうか
        self.assertContains(response,
                            "Juhacchu | Contact US")  # "order/icontact.html"に文字列："Juhacchu | Contact US"が含まれているか
        self.assertContains(response,
                            "メッセージを送信しました!!")  # "order/icontact.html"に文字列："メッセージを送信しました!!"が含まれているか
        self.assertContains(response,
                            'csrfmiddlewaretoken')  # "account/contact.html"に動的に生成される"csrfmiddlewaretoken"が含まれるか
        self.assertIsInstance(  # "response.context['form']"が"ContactForm"のインスタンスかどうか
            response.context['form'], ContactForm
        )

        # メールが送信されたか（厳密にはメールがoutboxに保存されたか）
        self.email = mail.outbox[0]

        self.assertEqual(len(mail.outbox), 1)  # 1件のメッセージ
        self.assertEqual(os.environ.get('DEFAULT_FROM_EMAIL'), self.email.to[0])  # 宛先メールアドレスが正しいかどうか
        self.assertEqual('test-contact-mail@example.com', self.email.from_email)
        self.assertEqual('お問い合せ お問い合わせメール送信テスト', self.email.subject)  # 件名が正しいかどうか

        email_confirmation_message = 'お問い合わせメール送信テスト'
        self.assertIn(email_confirmation_message, self.email.body)  # メール本文にemail_confirmation_messageが含まれるか

    # お問い合わせメール送信失敗テスト
    def test_contact_send_email(self):

        # ContactViewへpost_data_failureをポスト
        response = self.client.post(
            reverse("order:contact"),
            self.post_data_failure,
            follow=True
        )

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "order/contact.html")  # 使用テンプレートが"order/contact.html"かどうか
        self.assertContains(response,
                            "Juhacchu | Contact US")  # "order/contact.html"に文字列："Juhacchu | Contact US"が含まれているか
        self.assertNotContains(response,
                            "メッセージを送信しました!!")  # "order/contact.html"に文字列："メッセージを送信しました!!"が含まれているか
        self.assertContains(response,
                            'csrfmiddlewaretoken')  # "account/contact.html"に動的に生成される"csrfmiddlewaretoken"が含まれるか
        self.assertIsInstance(  # "response.context['form']"が"ContactForm"のインスタンスかどうか
            response.context['form'], ContactForm
        )

        self.assertEqual(len(mail.outbox), 0)  # mail.outboxにメッセージが1件もないかどうか


class TestPlacedOrderListView(TestCase):

    def setUp(self):

        """ログインユーザー001"""
        # test用ログインユーザ001のデータ
        self.test_user_data_001 = {
            "username": "testuser001",
            "email": "testuser001@example.com",
            "password": "abcdefg123456",
        }

        # テスト用ログインユーザーデータをデータベースに作成
        self.test_user_001 = get_user_model().objects.create_user(
            self.test_user_data_001['username'],
            self.test_user_data_001['email'],
            self.test_user_data_001['password']
        )

        # 新規ユーザが追加されたか
        self.assertTrue(
            CustomUser.objects.filter(
                email=self.test_user_data_001['email']
            ).exists()
        )

        """"""
        # ポストするログインユーザー001のメールアドレスとパスワードをpost_dataに格納
        post_data = {
            'email': self.test_user_data_001['email'],
            'password': self.test_user_data_001['password']
        }

        # ログイン loginメソッドを呼び出すことによってクッキーとセッションデータを取得
        login_status = self.client.login(email=self.test_user_data_001['email'],
                                         password=self.test_user_data_001['password'])
        self.assertTrue(login_status)

        self.client.post(
            reverse("account_login"),
            post_data,
            follow=True
        )

        # ログイン状態かどうか
        self.assertTrue(
            get_user(self.client).is_authenticated
        )

        """非ログインユーザー002"""
        # test用ログインユーザ002データ
        self.test_user_data_002 = {
            "username": "testuser002",
            "email": "testuser002@example.com",
            "password": "abcdefg123456",
        }

        # テスト用非ログインユーザー002データをデータベースに作成
        self.test_user_002 = get_user_model().objects.create_user(
            self.test_user_data_002['username'],
            self.test_user_data_002['email'],
            self.test_user_data_002['password']
        )

        # 新規ユーザが追加されたか
        self.assertTrue(
            CustomUser.objects.filter(
                email=self.test_user_data_002['email']
            ).exists()
        )

        # 発注商品001テストデータ
        self.placed_order_001 = {
            "buyer": self.test_user_001,
            "seller": self.test_user_002,
            "item_id": 0,
            "name": "テスト商品名001"
        }

        # ログインユーザー001の発注履歴データをデータベスに挿入
        self.test_order_001 = Order.objects.create(
            buyer=self.placed_order_001['buyer'],
            seller=self.placed_order_001['seller'],
            item_id=self.placed_order_001['item_id'],
            name=self.placed_order_001['name']
        )

        # 発注商品002テストデータ
        self.placed_order_002 = {
            "buyer": self.test_user_002,
            "seller": self.test_user_001,
            "item_id": 2,
            "name": "テスト商品名002"
        }

        # ログインユーザー001の発注履歴データをデータベスに挿入
        self.test_order_002 = Order.objects.create(
            buyer=self.placed_order_002['buyer'],
            seller=self.placed_order_002['seller'],
            item_id=self.placed_order_002['item_id'],
            name=self.placed_order_002['name']
        )

        # テスト用商品データが追加されたか
        self.assertTrue(
            Order.objects.filter(
                name=self.test_order_002.name
            ).exists()
        )

    def test_placed_order_list(self):

        # 発注履歴一覧ページを取得
        response = self.client.get(reverse("order:placed_order_list"))

        self.assertEqual(response.status_code, 200)

        # 使用テンプレートが"order/placed_order_list.html"かどうか
        self.assertTemplateUsed(
            response,
            "order/placed_order_list.html"
        )

        # "order/placed_order_list.html"に文字列："テスト商品名001"が含れているか
        self.assertContains(
            response,
            "テスト商品名001"
        )

        # "order/placed_order_list.html"に文字列："テスト商品名002"が含れていないか
        self.assertNotContains(
            response,
            "テスト商品名002"
        )


class TestOrderCreate(TestCase):

    def setUp(self):

        """ログインユーザー001"""
        # test用ログインユーザ001のデータ
        self.test_user_data_001 = {
            "username": "testuser001",
            "email": "testuser001@example.com",
            "password": "abcdefg123456",
        }

        # テスト用ログインユーザーデータをデータベースに作成
        self.test_user_001 = get_user_model().objects.create_user(
            self.test_user_data_001['username'],
            self.test_user_data_001['email'],
            self.test_user_data_001['password']
        )

        # 新規ユーザが追加されたか
        self.assertTrue(
            CustomUser.objects.filter(
                email=self.test_user_data_001['email']
            ).exists()
        )

        """"""
        # ポストするログインユーザー001のメールアドレスとパスワードをpost_dataに格納
        post_data = {
            'email': self.test_user_data_001['email'],
            'password': self.test_user_data_001['password']
        }

        # ログイン loginメソッドを呼び出すことによってクッキーとセッションデータを取得
        login_status = self.client.login(email=self.test_user_data_001['email'],
                                         password=self.test_user_data_001['password'])

        self.assertTrue(login_status)

        response = self.client.post(
            reverse("account_login"),
            post_data,
            follow=True
        )

        # ログイン状態かどうか
        self.assertTrue(
            get_user(self.client).is_authenticated
        )

        # テスト用商品データ
        self.test_item_data = {
            "user_id": self.test_user_001.pk,
            "name": "abcあいう商品名001",
            "price": 123,
            "unit": "本"
        }

        # テスト用商品データをデータベスに挿入
        self.item = Item.objects.create(
            user_id=self.test_item_data['user_id'],
            name=self.test_item_data['name'],
            price=self.test_item_data['price'],
            unit=self.test_item_data['unit']
        )

        # テスト用商品データが追加されたか
        self.assertTrue(
            Item.objects.filter(
                name=self.item.name
            ).exists()
        )

        # テスト用カートデータ
        self.test_cart_data = {
           "cart_id": self.client.session.session_key,
        }

        # テスト用カートデータをデータベースに挿入
        self.cart = Cart.objects.create(
            cart_id=self.test_cart_data["cart_id"]
        )

        # テスト用カートデータが追加されたか
        self.assertTrue(
            Cart.objects.filter(
                cart_id=self.cart.cart_id
            ).exists()
        )

        # テスト用カート商品データ
        self.test_cart_item_data = {
            "item": self.item,
            "cart": self.cart,
            "quantity": 2
        }

        # テスト用カート商品データをデータベースに挿入
        self.cart_item = CartItem.objects.create(
            item=self.test_cart_item_data["item"],
            cart=self.test_cart_item_data["cart"],
            quantity=self.test_cart_item_data["quantity"]

        )

        # テスト用カート商品データが追加されたか
        self.assertTrue(
            CartItem.objects.filter(
                cart=self.cart_item.cart
            ).exists()
        )

    def test_order_create(self):

        response = self.client.post(
            reverse("order:order_create"),
            self.test_cart_data,
            follow=True
        )

        self.assertRedirects(
            response,
            reverse('order:placed_order_list'),
            status_code=302,
            target_status_code=200,
            fetch_redirect_response=True
        )

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "order/placed_order_list.html")  # 使用テンプレートが"order/icontact.html"かどうか
        self.assertContains(response,
                            "abcあいう商品名001")  # "order/placed_order_list.html"に文字列："abcあいう商品名001"が含まれているか
        self.assertContains(response,
                            "発注が完了しました。")  # "order/placed_order_list.html"に文字列："発注が完了しました。"が含まれているか

        # メールが送信されたか（厳密にはメールがoutboxに保存されたか）
        self.email = mail.outbox[0]

        self.assertEqual(len(mail.outbox), 2)  # 1件のメッセージ
        self.assertEqual('testuser001@example.com', self.email.to[0])  # 宛先メールアドレスが正しいかどうか
        self.assertEqual(os.environ.get('DEFAULT_FROM_EMAIL'), self.email.from_email)
        self.assertEqual('Juhacchu 発注情報', self.email.subject)  # 件名が正しいかどうか
        self.assertIn('abcあいう商品名001 - 2', self.email.body)  # 本文に"abcあいう商品名001 - 2"が含まれているか
