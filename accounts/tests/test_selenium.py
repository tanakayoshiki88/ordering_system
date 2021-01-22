from django.test import LiveServerTestCase
from django.urls import reverse, reverse_lazy
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

    def test_login_logout(self):
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

        # id='userDropdown'をクリックしドロップダウンを表示
        self.selenium.find_element_by_id('userDropdown').click()
        # 表示されたドロップダウンの'Logout'をクリックしログアウト実行
        self.selenium.find_element_by_class_name('dropdown-logout').click()

        # ページタイトルの検証
        self.assertEqual('Login | Juhatchu', self.selenium.title)
