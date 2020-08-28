from django import forms
from django.core.mail import EmailMessage
from item.models import Item
from .models import Order


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


# オーダー編集フォーム
class OrderUpdateForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'

    class Meta:
        model = Order
        fields = '__all__'


# オーダー編集フォームセット
OrderUpdateFormSetBySeller = forms.modelformset_factory(Order, fields=('id', 'is_active',), form=OrderUpdateForm, extra=0)
