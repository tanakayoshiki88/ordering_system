from django.contrib.auth import get_user, get_user_model
from django.test import TestCase
from django.urls import reverse_lazy, reverse
from django.db.models import Q
from item.forms import ItemCreateForm, ItemUpdateForm

from accounts.models import CustomUser
from item.models import Item


class TestItemCreateView(TestCase):

    def setUp(self):

        # test用ユーザデータ
        self.test_user = {
            "username": "testuser001",
            "email": "testuser001@example.com",
            "password": "abcdefg123456",
        }

        # テスト用ユーザーデータをデータベースに作成
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

        # テスト用商品名
        self.item_data_for_test = {
            "name": "abcあいう商品名123",
            "price": 1,
            "unit": "本",
            "stock": 1,
        }

        # テスト用商品名
        self.item_data_for_test_failure = {
            "name": "abcあいう商品名123",
            "price": 1,
        }

    # 非ログイン状態で商品登録ページのロードをして"/accounts/login/?next=/item/item-create/"へリダイレクトされるか
    def test_item_create_page_loads_failure(self):
        response = self.client.get('/item/item-create/',)

        # "/accounts/login/?next=/item/item-create/"へリダイレクトされたか
        self.assertRedirects(
            response,
            '/accounts/login/?next=/item/item-create/',
            status_code=302,
            target_status_code=200,
            fetch_redirect_response=True
        )

        # ポストするメールアドレスとパスワードをpost_dataに格納
        post_data = {
            'email': self.test_user['email'],
            'password': self.test_user['password']
        }

        # "/accounts/login/?next=/item/item-create/"からログイン
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

    # ログイン状態で商品登録ページのロードし商品登録に成功するか
    def test_item_create_successfully(self):

        # ポストするメールアドレスとパスワードをpost_dataに格納
        post_data = {
            'email': self.test_user['email'],
            'password': self.test_user['password']
        }

        # ログイン loginメソッドを呼び出すことによってクッキーとセッションデータを取得
        login_status = self.client.login(email=self.test_user['email'], password=self.test_user['password'])
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

        # /index/へリダイレクトされたか
        self.assertRedirects(
            response,
            '/index/',
            status_code=302,
            target_status_code=200,
            fetch_redirect_response=True
        )

        # "/item/item-create/"をロードできるかどうか
        response = self.client.get('/item/item-create/')


        self.assertEqual(response.status_code, 200)  # ステータスコードが200かどうか
        self.assertTemplateUsed(response, 'item/item_create.html')  # 使用テンプレートが"account/password_reset.html"かどうか
        self.assertContains(response, '商品登録 | Juhatchu')  # "account/item_create.html"に動的に生成される"ログイン状態を維持する"が含まれるか
        self.assertContains(response, 'csrfmiddlewaretoken')  # "account/password_reset.html"に動的に生成される"csrfmiddlewaretoken"が含まれるか
        self.assertIsInstance(  # "response.context['form']"が"ResetPasswordForm"のインスタンスかどうか
            response.context['form'], ItemCreateForm
        )

        # ItemCreateViewへ商品名をポスト
        response = self.client.post(
            reverse('item:item_create'),
            self.item_data_for_test
        )

        # 新規商品が登録されたか
        self.assertTrue(
            Item.objects.filter(
                name=self.item_data_for_test['name']
            ).exists()
        )

        # /index/へリダイレクトされたか
        self.assertRedirects(
            response,
            reverse_lazy('item:item_list'),
            status_code=302,
            target_status_code=200,
            fetch_redirect_response=True
        )

    def test_item_create_failure(self):

        # ポストするメールアドレスとパスワードをpost_dataに格納
        post_data = {
            'email': self.test_user['email'],
            'password': self.test_user['password']
        }

        # ログイン loginメソッドを呼び出すことによってクッキーとセッションデータを取得
        login_status = self.client.login(email=self.test_user['email'], password=self.test_user['password'])
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

        # /index/へリダイレクトされたか
        self.assertRedirects(
            response,
            '/index/',
            status_code=302,
            target_status_code=200,
            fetch_redirect_response=True
        )

        # "/item/item-create/"をロードできるかどうか
        response = self.client.get('/item/item-create/')

        self.assertEqual(response.status_code, 200)  # ステータスコードが200かどうか
        self.assertTemplateUsed(response, 'item/item_create.html')  # 使用テンプレートが"account/password_reset.html"かどうか
        self.assertContains(response, '商品登録 | Juhatchu')  # "account/item_create.html"に動的に生成される"ログイン状態を維持する"が含まれるか
        self.assertContains(response, 'csrfmiddlewaretoken')  # "account/password_reset.html"に動的に生成される"csrfmiddlewaretoken"が含まれるか
        self.assertIsInstance(  # "response.context['form']"が"ResetPasswordForm"のインスタンスかどうか
            response.context['form'], ItemCreateForm
        )

        # ItemCreateViewへ商品名をポスト
        self.client.post(
            reverse('item:item_create'),
            self.item_data_for_test_failure
        )

        # 新規商品が登録されたか
        self.assertFalse(
            Item.objects.filter(
                name=self.item_data_for_test['name']
            ).exists()
        )


class TestItemList(TestCase):

    def setUp(self):
        # test用ユーザデータ
        self.test_user_data = {
            "username": "testuser001",
            "email": "testuser001@example.com",
            "password": "abcdefg123456",
        }

        # テスト用ユーザーデータをデータベースに作成
        self.test_user = get_user_model().objects.create_user(
            self.test_user_data['username'],
            self.test_user_data['email'],
            self.test_user_data['password']
        )

        # 新規ユーザが追加されたか
        self.assertTrue(
            CustomUser.objects.filter(
                email=self.test_user_data['email']
            ).exists()
        )

        # ポストするメールアドレスとパスワードをpost_dataに格納
        post_data = {
            'email': self.test_user_data['email'],
            'password': self.test_user_data['password']
        }

        # ログイン loginメソッドを呼び出すことによってクッキーとセッションデータを取得
        login_status = self.client.login(email=self.test_user_data['email'], password=self.test_user_data['password'])
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

    def test_item_create_page_loads_failure(self):

        # "item:item_list"を取得
        response = self.client.get(
            reverse('item:item_list')
        )

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'item/item_list.html')
        self.assertContains(response, "まだ商品が登録されておりません。")

    def test_item_create_page_loads_successfully(self):

        # テスト用商品名
        self.item_data_for_test = {
            "user_id": self.test_user.pk,
            "name": "abcあいう商品名123",
            "price": 1,
            "unit": "本"
        }

        # テスト用商品データをデータベスに挿入
        Item.objects.create(
            user_id=self.item_data_for_test['user_id'],
            name=self.item_data_for_test['name'],
            price=self.item_data_for_test['price'],
            unit=self.item_data_for_test['unit']
        )

        # ポストするメールアドレスとパスワードをpost_dataに格納
        post_data = {
            'email': self.test_user_data['email'],
            'password': self.test_user_data['password']
        }

        # ログイン loginメソッドを呼び出すことによってクッキーとセッションデータを取得
        login_status = self.client.login(email=self.test_user_data['email'], password=self.test_user_data['password'])
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

        response = self.client.get(
            reverse('item:item_list')
        )

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'item/item_list.html')
        self.assertContains(response, "abcあいう商品名123")


class TestItemDetailView(TestCase):

    def setUp(self):
        # test用ユーザデータ
        self.test_user_data = {
            "username": "testuser001",
            "email": "testuser001@example.com",
            "password": "abcdefg123456",
        }

        # テスト用ユーザーデータをデータベースに作成
        self.test_user = get_user_model().objects.create_user(
            self.test_user_data['username'],
            self.test_user_data['email'],
            self.test_user_data['password']
        )

        # 新規ユーザが追加されたか
        self.assertTrue(
            CustomUser.objects.filter(
                email=self.test_user_data['email']
            ).exists()
        )

        # ポストするメールアドレスとパスワードをpost_dataに格納
        post_data = {
            'email': self.test_user_data['email'],
            'password': self.test_user_data['password']
        }

        # ログイン loginメソッドを呼び出すことによってクッキーとセッションデータを取得
        login_status = self.client.login(email=self.test_user_data['email'], password=self.test_user_data['password'])
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

    def test_item_create_page_loads_successfully(self):

        # テスト用商品名
        self.item_data_for_test = {
            "user_id": self.test_user.pk,
            "name": "abcあいう商品名123",
            "price": 1,
            "unit": "本"
        }

        # テスト用商品データをデータベスに挿入
        test_item = Item.objects.create(
            user_id=self.item_data_for_test['user_id'],
            name=self.item_data_for_test['name'],
            price=self.item_data_for_test['price'],
            unit=self.item_data_for_test['unit']
        )

        # ポストするメールアドレスとパスワードをpost_dataに格納
        post_data = {
            'email': self.test_user_data['email'],
            'password': self.test_user_data['password']
        }

        # ログイン loginメソッドを呼び出すことによってクッキーとセッションデータを取得
        login_status = self.client.login(email=self.test_user_data['email'], password=self.test_user_data['password'])
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

        response = self.client.get(
            reverse('item:item_detail', args=[test_item.pk])
        )

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'item/item_detail.html')
        self.assertContains(response, "abcあいう商品名123")


class TestItemUpdateView(TestCase):

    def setUp(self):

        # test用ユーザデータ
        self.test_user_data = {
            "username": "testuser001",
            "email": "testuser001@example.com",
            "password": "abcdefg123456",
        }

        # テスト用ユーザーデータをデータベースに作成
        self.test_user = get_user_model().objects.create_user(
            self.test_user_data['username'],
            self.test_user_data['email'],
            self.test_user_data['password']
        )

        # 新規ユーザが追加されたか
        self.assertTrue(
            CustomUser.objects.filter(
                email=self.test_user_data['email']
            ).exists()
        )

        # ポストするメールアドレスとパスワードをpost_dataに格納
        post_data = {
            'email': self.test_user_data['email'],
            'password': self.test_user_data['password']
        }

        # ログイン loginメソッドを呼び出すことによってクッキーとセッションデータを取得
        login_status = self.client.login(email=self.test_user_data['email'], password=self.test_user_data['password'])
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

        # テスト用商品名
        self.item_data_for_test = {
            "user_id": self.test_user.pk,
            "name": "abcあいう商品名123",
            "price": 1,
            "unit": "本",
            "stock": 1
        }

        # テスト用商品データをデータベースに挿入
        self.test_item = Item.objects.create(
            user_id=self.item_data_for_test['user_id'],
            name=self.item_data_for_test['name'],
            price=self.item_data_for_test['price'],
            unit=self.item_data_for_test['unit']
        )

    def test_item_update_page_loads(self):

        # "item/item-update/<self.test_item.pk"へgetリクエストを送りresponseオブジェクトを受け取る
        response = self.client.get(
            reverse('item:item_update', args=[self.test_item.pk])
        )

        self.assertEqual(response.status_code, 200)  # 正常にページが表示されたか
        self.assertTemplateUsed(response, 'item/item_update.html')  # "item/item_update.html"がテンプレートとして使用されたか
        self.assertContains(response, "abcあいう商品名123")  # response.contentのなかに"abcあいう商品名123"が含まれているか
        self.assertIsInstance(  # "response.context['form']"が"SignupForm"のインスタンスかどうか
            response.context['form'], ItemUpdateForm
        )

    def test_item_update_successfully(self):

        # "item/item-update/<self.test_item.pk"へgetリクエストを送りresponseオブジェクトを受け取る
        response = self.client.get(
            reverse('item:item_update', args=[self.test_item.pk])
        )

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'item/item_update.html')  # "item/item_update.html"がテンプレートとして使用されたか
        self.assertContains(response, "abcあいう商品名123")  # response.contentのなかに"abcあいう商品名123"が含まれているか

        redirect_url = '/item/item-detail/' + str(self.test_item.pk) + '/'

        response = self.client.post(
            reverse('item:item_update', kwargs={'pk': self.test_item.pk}),
            self.item_data_for_test,
            follow=True
        )

        # redirect_urlへリダイレクトされたか
        self.assertRedirects(
            response,
            redirect_url,
            status_code=302,
            target_status_code=200,
            fetch_redirect_response=True
        )


class TestItemDeleteView(TestCase):

    def setUp(self):
        # test用ユーザデータ
        self.test_user_data = {
            "username": "testuser001",
            "email": "testuser001@example.com",
            "password": "abcdefg123456",
        }

        # テスト用ユーザーデータをデータベースに作成
        self.test_user = get_user_model().objects.create_user(
            self.test_user_data['username'],
            self.test_user_data['email'],
            self.test_user_data['password']
        )

        # 新規ユーザが追加されたか
        self.assertTrue(
            CustomUser.objects.filter(
                email=self.test_user_data['email']
            ).exists()
        )

        # ポストするメールアドレスとパスワードをpost_dataに格納
        post_data = {
            'email': self.test_user_data['email'],
            'password': self.test_user_data['password']
        }

        # ログイン loginメソッドを呼び出すことによってクッキーとセッションデータを取得
        login_status = self.client.login(email=self.test_user_data['email'], password=self.test_user_data['password'])
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

        # テスト用商品名
        self.item_data_for_test = {
            "user_id": self.test_user.pk,
            "name": "abcあいう商品名123",
            "price": 1,
            "unit": "本"
        }

        # テスト用商品データをデータベスに挿入
        self.test_item = Item.objects.create(
            user_id=self.item_data_for_test['user_id'],
            name=self.item_data_for_test['name'],
            price=self.item_data_for_test['price'],
            unit=self.item_data_for_test['unit']
        )

        # テスト用商品データが追加されたか
        self.assertTrue(
            Item.objects.filter(
                name=self.test_item.name
            ).exists()
        )

    def test_item_delete_page_loads(self):

        # "item/item-update/<self.test_item.pk>"へgetリクエストを送りresponseオブジェクトを受け取る
        response = self.client.get(
            reverse('item:item_delete', args=[self.test_item.pk])
        )

        self.assertEqual(response.status_code, 200)  # 正常にページが表示されたか
        self.assertTemplateUsed(response, 'item/item_delete.html')  # "item/item_update.html"がテンプレートとして使用されたか
        self.assertContains(response, "abcあいう商品名123")  # response.contentのなかに"abcあいう商品名123"が含まれているか
        self.assertContains(response, "以下の商品をほんとうに削除しますか？")  # response.contentのなかに"以下の商品をほんとうに削除しますか？"が含まれているか
        self.assertContains(response, "csrfmiddlewaretoken")  # response.contentのなかに"csrfmiddlewaretoken"が含まれているか


    def test_item_delete_successfully(self):

        # ItemDeleteViewへ削除をポスト
        response = self.client.post(
            reverse('item:item_delete', args=[self.test_item.pk])
        )

        # テスト用商品データが削除されたか
        self.assertFalse(
            Item.objects.filter(
                name=self.test_item.name
            ).exists()
        )

        redirect_url = reverse('item:item_list')

        # reverse('item:item_list')へリダイレクトされたか
        self.assertRedirects(
            response,
            redirect_url,
            status_code=302,
            target_status_code=200,
            fetch_redirect_response=True
        )


class TestOrderItemListView(TestCase):

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

        """ログインユーザー001のテスト用商品データ"""
        # ログインユーザー001のテスト用商品データ
        self.item_data_for_test_001 = {
            "user_id": self.test_user_001.pk,
            "name": "abcあいう商品名001",
            "price": 1,
            "unit": "本"
        }

        # ログインユーザー001のテスト用商品データをデータベスに挿入
        self.test_item_001 = Item.objects.create(
            user_id=self.item_data_for_test_001['user_id'],
            name=self.item_data_for_test_001['name'],
            price=self.item_data_for_test_001['price'],
            unit=self.item_data_for_test_001['unit']
        )

        # テスト用商品データが追加されたか
        self.assertTrue(
            Item.objects.filter(
                name=self.test_item_001.name
            ).exists()
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

        """非ログインユーザー002のテスト用商品データ"""
        # 非ログインユーザー002のテスト用商品データ
        self.item_data_for_test_002 = {
            "user_id": self.test_user_002.pk,
            "name": "abcあいう商品名002",
            "price": 2,
            "unit": "束"
        }

        # 非ログインユーザー002のテスト用商品データをデータベスに挿入
        self.test_item_002 = Item.objects.create(
            user_id=self.item_data_for_test_002['user_id'],
            name=self.item_data_for_test_002['name'],
            price=self.item_data_for_test_002['price'],
            unit=self.item_data_for_test_002['unit']
        )

        # テスト用商品データが追加されたか
        self.assertTrue(
            Item.objects.filter(
                name=self.test_item_002.name
            ).exists()
        )

    def test_order_item_list_page_loads(self):
        # "item/order-item-list/<self.test_item_001.pk>"へgetリクエストを送りresponseオブジェクトを受け取る
        response = self.client.get(
            reverse('item:order_item_list')
        )

        self.assertEqual(response.status_code, 200)  # 正常にページが表示されたか
        self.assertTemplateUsed(response, 'item/order_item_list.html')  # "item/order_item_list.html"がテンプレートとして使用されたか
        self.assertContains(response, "abcあいう商品名002")  # response.contentのなかに"abcあいう商品名001"が含まれているか
        self.assertContains(response, self.test_item_002.pk)  # response.contentのなかに"self.test_item_002.pk"が含まれているか
        self.assertNotContains(response, "abcあいう商品名001")  # response.contentのなかに"abcあいう商品名001"が含まれていないか


class TestSearchItemListView(TestCase):

    # セットアップ
    def setUp(self):
        test_users = []
        test_items = []

        # test用ログインユーザ001のデータ
        self.test_user_data_001 = CustomUser(
            username='testuser001',
            email='testuser001@example.com',
            password='abcdefg123456',
        )

        # test用ログインユーザ002のデータ
        self.test_user_data_002 = CustomUser(
            username='testuser002',
            email='testuser002@example.com',
            password='hijklmn7890',
        )

        # リストに追加
        test_users.append(
            self.test_user_data_001
        )

        # リストに追加
        test_users.append(
            self.test_user_data_002
        )

        # ユーザデータ作成
        CustomUser.objects.bulk_create(test_users)

        # 新規ユーザ'test_user_data_001'が追加されたか
        self.assertTrue(
            CustomUser.objects.filter(
                email='testuser001@example.com'
            ).exists()
        )

        # 新規ユーザ'test_user_data_002'が追加されたか
        self.assertTrue(
            CustomUser.objects.filter(
                email='testuser002@example.com'
            ).exists()
        )

        # test用商品データ001
        self.test_item_data_001 = Item(
            user_id=self.test_user_data_001.pk,
            name='abcあいう商品名001',
            price=1,
            unit='束'
        )

        # test用商品データ002
        self.test_item_data_002 = Item(
            user_id=self.test_user_data_002.pk,
            name='abcあいう商品名002',
            price=2,
            unit='個'
        )

        # リストに追加
        test_items.append(
            self.test_item_data_001
        )

        # リストに追加
        test_items.append(
            self.test_item_data_002
        )

        # 商品データ作成
        Item.objects.bulk_create(test_items)

        # 新規商品データ'test_item_data_001'が追加されたか
        self.assertTrue(
            Item.objects.filter(
                name='abcあいう商品名001'
            ).exists()
        )

        # 新規商品データ'test_item_data_002'が追加されたか
        self.assertTrue(
            Item.objects.filter(
                name='abcあいう商品名002'
            ).exists()
        )

    def test_item_search(self):

        # ログインしていないユーザーによる検索
        response = self.client.get('/item/search-item-list/', {'query': 'cあいう商品名001'})

        self.assertEqual(response.status_code, 200)  # 正常にページが表示されたか
        self.assertTemplateUsed(response, 'item/search_item_list.html')  # "item/search_item_list.html"がテンプレートとして使用されたか
        self.assertContains(response, "abcあいう商品名001")  # response.contentのなかに"abcあいう商品名001"が含まれているか
        self.assertContains(response, self.test_item_data_001.pk)  # response.contentのなかに"self.test_item_001.pk"が含まれているか
        self.assertNotContains(response, "abcあいう商品名002")  # response.contentのなかに"abcあいう商品名002"が含まれていないか
