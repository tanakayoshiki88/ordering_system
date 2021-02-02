from django.test import LiveServerTestCase
from django.urls import reverse
from selenium.webdriver.chrome.webdriver import WebDriver

import os


class TestLogin(LiveServerTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.selenium = WebDriver()  # webdriverの配置場所が環境変数＄PATHにエクスポートしていない場合は、executable_path='ドライバ配置場所'


    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super().tearDownClass()

    def setUp(self):
        # ログインページを表示
        self.selenium.get("http://localhost:8000" + str(reverse('account_login')))

        # ログイン実行
        username_input = self.selenium.find_element_by_name('login')
        username_input.send_keys(os.environ.get('DEFAULT_FROM_EMAIL'))
        username_input = self.selenium.find_element_by_name('password')
        username_input.send_keys(os.environ.get('SELENIUM_TEST_PASSWORD'))
        self.selenium.find_element_by_class_name('btn').click()

        # ページタイトルの検証
        self.assertEqual('INDEX | Juhatchu', self.selenium.title)

        # base.htmlのカートアイコン押下
        self.selenium.find_element_by_css_selector('#cart-icon a').click()

        # すべての商品削除ボタンをクリックしてカートを空にする
        for cart_item_remove in self.selenium.find_elements_by_class_name('item-remove'):
            cart_item_remove.click()
        else:
            pass

        # cart.htmlの表示確認 'Your shopping cart is empty'が表示されているか
        self.assertIn('Your shopping cart is empty', self.selenium.page_source)

    def test_cart_view(self):
        # ログインページを表示
        self.selenium.get("http://localhost:8000")

        # ページタイトルの検証
        self.assertEqual('INDEX | Juhatchu', self.selenium.title)

        # 購入商品一覧画面を取得
        self.selenium.get("http://localhost:8000" + str(reverse('item:order_item_list')))

        # class='pagination'の2ページ目をクリック
        pagination_li_2 = self.selenium.find_element_by_css_selector('.pagination li:nth-child(2)').click()
        # ページに含まれる文字の検証
        self.assertIn('«', self.selenium.page_source)

        # id='dataTable'の商品詳細ページ遷移ボタンをクリック
        self.selenium.find_element_by_css_selector('#dataTable tbody tr:nth-child(1) td:nth-child(7) a').click()
        # ページタイトルの検証
        self.assertEqual('商品詳細 | Juhatchu', self.selenium.title)
        # ページに含まれる文字列の検証
        self.assertIn('カートに追加', self.selenium.page_source)

        # class='add-cart-button'(カートに追加)をクリック
        self.selenium.find_element_by_css_selector('.add-cart-button a').click()
        # ページタイトルの検証
        self.assertEqual('ショッピングカート | Juhatchu', self.selenium.title)
        # ページに含まれる文字列の検証
        self.assertIn('ショッピングカートの商品を確認してください', self.selenium.page_source)

        # class='increase-quantity'をクリックする前の数量を取得し、1を足す
        before_quantity = int(self.selenium.find_element_by_id('item-quantity').text)
        result_quantity = str(before_quantity + 1)
        # class='increase-quantity'をクリック
        self.selenium.find_element_by_css_selector('.increase-quantity').click()
        # 表示されている数量を取得
        after_quantity = self.selenium.find_element_by_id('item-quantity')
        # 数量result_quantityとafter_quantityが等しいかどうか検証
        self.assertEqual(result_quantity, after_quantity.text)
        # class='reduce-quantity'をクリックし数量を減らす
        self.selenium.find_element_by_css_selector('.reduce-quantity').click()
        # 表示されている数量を取得
        quantity = int(self.selenium.find_element_by_id('item-quantity').text)
        # 数量が1かどうか検証
        self.assertEqual(before_quantity, quantity)
        # class='item-remove'をクリックし商品を削除
        self.selenium.find_element_by_css_selector('.item-remove').click()
        # ページに含まれる文字列の検証
        self.assertIn('Your shopping cart is empty', self.selenium.page_source)

        """ 改めて購入商品一覧画面を取得 """
        self.selenium.get("http://localhost:8000" + str(reverse('item:order_item_list')))

        # id='dataTable'の商品詳細ページ遷移ボタンをクリック
        self.selenium.find_element_by_css_selector('#dataTable tbody tr:nth-child(1) td:nth-child(2) a').click()
        # ページタイトルの検証
        self.assertEqual('商品詳細 | Juhatchu', self.selenium.title)
        # ページに含まれる文字列の検証
        self.assertIn('カートに追加', self.selenium.page_source)

        # class='add-cart-button'(カートに追加)をクリック
        self.selenium.find_element_by_css_selector('.add-cart-button a').click()
        # ページタイトルの検証
        self.assertEqual('ショッピングカート | Juhatchu', self.selenium.title)
        # ページに含まれる文字列の検証
        self.assertIn('ショッピングカートの商品を確認してください', self.selenium.page_source)

        # class='order-confirm'(発注確認画面へ>>)をクリック
        self.selenium.find_element_by_css_selector('.order-confirm').click()
        # ページタイトルの検証
        self.assertEqual('発注確認 | Juhatchu', self.selenium.title)
        # ページに含まれる文字列の検証
        self.assertIn('ショッピングカートの商品を確認してください', self.selenium.page_source)
