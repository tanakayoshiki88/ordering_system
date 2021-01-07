from django.contrib.auth import get_user, get_user_model
from django.test import TestCase
from django.urls import reverse


from accounts.models import CustomUser
from item.models import Item
from cart.models import Cart, CartItem


class TestAddCart(TestCase):

    """商品カート追加機能テスト"""
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

        # ログイン loginメソッドを呼び出すことによってクッキーとセッションデータを取得
        login_status = self.client.login(email=self.test_user_data_001['email'],
                                         password=self.test_user_data_001['password'])

        client_request = self.client.request

        self.assertTrue(login_status)

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

    def test_add_create(self):

        request = {
            "session_key": self.client.session.session_key
        }

        response = self.client.post(
            reverse('cart:add_cart', kwargs={'item_id': self.item.id}),
            request,
            follow=True
        )

        # 新規カートデータが追加されたか
        self.assertTrue(
            Cart.objects.filter(
                cart_id=request["session_key"]
            ).exists()
        )

        pk = Cart.objects.get(cart_id=request["session_key"]).pk

        # 新規カートデータが追加されたか
        self.assertTrue(
            CartItem.objects.filter(
                cart=pk
            ).exists()
        )

        # redirect('cart:cart_detail')へリダイレクトされたか
        self.assertRedirects(
            response,
            reverse('cart:cart_detail'),
            status_code=302,
            target_status_code=200,
            fetch_redirect_response=True
        )

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "cart.html")  # 使用テンプレートが"order/placed_order_list.html"かどうか
        self.assertContains(
            response,
            "ご注文のお支払いに進む前に、ショッピングカートの商品を確認してください"
        )  # "order/placed_order_list.html"に文字列：""ご注文のお支払いに進む前に、ショッピングカートの商品を確認してください"が含まれているか
        self.assertContains(
            response,
            "abcあいう商品名001")  # "order/placed_order_list.html"に文字列："abcあいう商品名001"が含まれているか
        self.assertContains(
            response,
            '135')  # "account/placed_order_list.html"に動的に生成される合計金額"135"(123*1.1)が含まれるか
