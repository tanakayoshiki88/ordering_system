from django import forms
from django.core.mail import EmailMessage
from .models import Item, Order, FavoriteItem
from accounts.models import CustomUser
from django.db.models import Avg, Max, Min, Sum


# 問合せフォーム
class ContactForm(forms.Form):
    last_name = forms.CharField(label='', max_length=30)
    first_name = forms.CharField(label='', max_length=30)
    email = forms.EmailField(label='',)
    subject = forms.CharField(label='', max_length=30)
    message = forms.CharField(label='', widget=forms.Textarea)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['last_name'].widget.attrs['class'] = 'form-control form-control-user'
        self.fields['last_name'].widget.attrs['placeholder'] = 'Last Name'

        self.fields['first_name'].widget.attrs['class'] = 'form-control form-control-user'
        self.fields['first_name'].widget.attrs['placeholder'] = 'First Name'

        self.fields['email'].widget.attrs['class'] = 'form-control form-control-user'
        self.fields['email'].widget.attrs['placeholder'] = 'Email Address'

        self.fields['subject'].widget.attrs['class'] = 'form-control form-control-user'
        self.fields['subject'].widget.attrs['placeholder'] = 'Subject'

        self.fields['message'].widget.attrs['class'] = 'form-control form-control-user'
        self.fields['message'].widget.attrs['id'] = 'id_message'
        self.fields['message'].widget.attrs['rows'] = '5'
        self.fields['message'].widget.attrs['placeholder'] = 'Message'

    #   メール送信関数
    def send_email(self):
        name = self.cleaned_data['last_name'] + " " + self.cleaned_data['first_name']
        email = self.cleaned_data['email']
        subject = self.cleaned_data['subject']
        message = self.cleaned_data['message']

        subject = 'お問い合せ {}'.format(subject)
        message = '送信者名： {0}\nメッセージ：\n{2}'.format(name, email, message)
        from_email = 'example@gmail.com'
        to_list = [
            'test@example.com'
        ]
        cc_list = [
            email
        ]

        message = EmailMessage(subject=subject, body=message, from_email=from_email, to=to_list, cc=cc_list)

        message.send()


'''class OderForm(forms.Form):
    quantity = forms.IntegerField(label='',)
    delivery_date = forms.DateTimeField(label='')
'''
class ItemCreateForm(forms.ModelForm):
    # 商品登録フォーム
    class Meta:
        model = Item
        fields = (
                    "name",
                    "price",
                    "including_tax",
                    "unit",
                    "stock",
                    "moq",
                    "spq",
                    "category1",
                    "category2",
                    "category3",
                    "is_active",
                    "photo"
        )

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            for field in self.fields.values():
                field.widget.attrs['class'] = 'form-control form-control-user'


'''    name = forms.CharField(label='商品名', max_length=40, required=True)
    price = forms.IntegerField(label='単価', required=True)
    including_tax = forms.BooleanField(label='税込', required=True)
    unit = forms.CharField(label='単位', max_length=10)
    stock = forms.IntegerField(label='在庫数')
    category1 = forms.CharField(label='カテゴリ1', max_length=30)
    category2 = forms.CharField(label='カテゴリ2', max_length=30)
    category3 = forms.CharField(label='カテゴリ3', max_length=30)
    photo = forms.ImageField(label='商品画像')


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['name'].widget.attrs['class'] = 'form-control form-control-user'
        self.fields['name'].widget.attrs['placeholder'] = 'Item Name'

        self.fields['price'].widget.attrs['class'] = 'form-control form-control-user'
        self.fields['price'].widget.attrs['placeholder'] = 'Price'

        self.fields['including_tax'].widget.attrs['class'] = 'form-control form-control-user'
        self.fields['including_tax'].widget.attrs['placeholder'] = 'Tax'

        self.fields['unit'].widget.attrs['class'] = 'form-control form-control-user'
        self.fields['unit'].widget.attrs['placeholder'] = 'Unit'

        self.fields['stock'].widget.attrs['class'] = 'form-control form-control-user'
        self.fields['stock'].widget.attrs['placeholder'] = 'Stock'

        self.fields['category1'].widget.attrs['class'] = 'form-control form-control-user'
        self.fields['category1'].widget.attrs['placeholder'] = 'Category1'

        self.fields['category2'].widget.attrs['class'] = 'form-control form-control-user'
        self.fields['category2'].widget.attrs['placeholder'] = 'Category2'

        self.fields['category3'].widget.attrs['class'] = 'form-control form-control-user'
        self.fields['category3'].widget.attrs['placeholder'] = 'Category3'

        self.fields['photo'].widget.attrs['class'] = 'form-control form-control-user'
        self.fields['photo'].widget.attrs['placeholder'] = 'Photo'
'''

class ItemUpdateForm(forms.ModelForm):
    # 商品登録フォーム
    class Meta:
        model = Item
        fields = (
                    "name",
                    "price",
                    "including_tax",
                    "unit",
                    "stock",
                    "moq",
                    "spq",
                    "category1",
                    "category2",
                    "category3",
                    "is_active",
                    "photo"
        )


'''    name = forms.CharField(label='商品名', max_length=40, required=True)
    price = forms.IntegerField(label='単価', required=True)
    including_tax = forms.BooleanField(label='税込', required=True)
    unit = forms.CharField(label='単位', max_length=10)
    stock = forms.IntegerField(label='在庫数')
    category1 = forms.CharField(label='カテゴリ1', max_length=30)
    category2 = forms.CharField(label='カテゴリ2', max_length=30)
    category3 = forms.CharField(label='カテゴリ3', max_length=30)
    photo = forms.ImageField(label='商品画像')


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['name'].widget.attrs['class'] = 'form-control form-control-user'
        self.fields['name'].widget.attrs['placeholder'] = 'Item Name'

        self.fields['price'].widget.attrs['class'] = 'form-control form-control-user'
        self.fields['price'].widget.attrs['placeholder'] = 'Price'

        self.fields['including_tax'].widget.attrs['class'] = 'form-control form-control-user'
        self.fields['including_tax'].widget.attrs['placeholder'] = 'Tax'

        self.fields['unit'].widget.attrs['class'] = 'form-control form-control-user'
        self.fields['unit'].widget.attrs['placeholder'] = 'Unit'

        self.fields['stock'].widget.attrs['class'] = 'form-control form-control-user'
        self.fields['stock'].widget.attrs['placeholder'] = 'Stock'

        self.fields['category1'].widget.attrs['class'] = 'form-control form-control-user'
        self.fields['category1'].widget.attrs['placeholder'] = 'Category1'

        self.fields['category2'].widget.attrs['class'] = 'form-control form-control-user'
        self.fields['category2'].widget.attrs['placeholder'] = 'Category2'

        self.fields['category3'].widget.attrs['class'] = 'form-control form-control-user'
        self.fields['category3'].widget.attrs['placeholder'] = 'Category3'

        self.fields['photo'].widget.attrs['class'] = 'form-control form-control-user'
        self.fields['photo'].widget.attrs['placeholder'] = 'Photo'
'''

class OrderCreateForm(forms.ModelForm):
    # 発注フォーム
    class Meta:
        model = Order
        fields = (
            "item",
            "quantity",
            "remarks"
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        item_pk = Item.objects.values('pk').order_by('pk')
        i = 0

        for field in self.fields.values():
            field.widget.attrs['class'] = "form-control form-control-user"
            field.widget.attrs['rows'] = "1rem"
            field.widget.attrs['id'] = "id_item"
            field.widget.attrs['value'] = item_pk[i]['pk']
            i += 1


# OderCreateFormのモデルフォームセット
OrderCreateFormSet = forms.modelformset_factory(
    Order, form=OrderCreateForm, extra=Item.objects.all().count()
)


class FavoriteItemCreateForm(forms.ModelForm):
    # 発注商品リスト登録
    class Meta:
        model = FavoriteItem
        fields = (
            "user",
            "item"
        )
