from allauth.account.forms import SignupForm
from allauth.account.forms import LoginForm
from allauth.account.forms import ResetPasswordForm
from allauth.account.forms import ResetPasswordKeyForm


class CustomSignupForm(SignupForm):

    def __init__(self, *args, **kwargs):
        super(CustomSignupForm, self).__init__(*args, **kwargs)

        # すべてのフィールドにクラス属性を設定
        for fieldname, field in self.fields.items():
            field.widget.attrs.update({
                'class': 'form-control form-control-user',
            })

        # 'email' フィールドに 'placeholder'属性を設定
        self.fields['email'].widget.attrs.update({
            'placeholder': 'Email Address',
        })

        # 'password1' フィールドに 'placeholder'属性を設定
        self.fields['password1'].widget.attrs.update({
            'placeholder': 'Password',
        })

        # 'password2' フィールドに 'placeholder'属性を設定
        self.fields['password2'].widget.attrs.update({
            'placeholder': 'Repeat Password',
        })


class CustomLoginForm(LoginForm):

    def __init__(self, *args, **kwargs):
        super(CustomLoginForm, self).__init__(*args, **kwargs)

        # すべてのフィールドにクラス属性を設定
#        for fieldname, field in self.fields.items():
#            field.widget.attrs.update({
#                'class': 'form-control form-control-user',
#            })

        # 'email' フィールドに 'placeholder'属性を設定
        self.fields['login'].widget.attrs.update({
            'placeholder': 'Email Address',
            'class': 'form-control form-control-user'
        })

        # 'password' フィールドに 'placeholder'属性を設定
        self.fields['password'].widget.attrs.update({
            'placeholder': 'Password',
            'class': 'form-control form-control-user'
        })

class CustomResetPasswordForm(ResetPasswordForm):

    def __init__(self, *args, **kwargs):
        super(CustomResetPasswordForm, self).__init__(*args, **kwargs)

        # 'email' フィールドに 'placeholder'属性を設定
        self.fields['email'].widget.attrs.update({
            'placeholder': 'Email Address',
            'class': 'form-control form-control-user'
        })


class CustomResetPasswordKeyForm(ResetPasswordKeyForm):

    def __init__(self, *args, **kwargs):
        super(CustomResetPasswordKeyForm, self).__init__(*args, **kwargs)

        # 'email' フィールドに 'placeholder'属性を設定
        self.fields['password1'].widget.attrs.update({
            'placeholder': 'New Password',
            'class': 'form-control form-control-user'
        })

        # 'email' フィールドに 'placeholder'属性を設定
        self.fields['password2'].widget.attrs.update({
            'placeholder': 'New Password(again)',
            'class': 'form-control form-control-user'
        })