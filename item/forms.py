from django import forms
from item.models import Item


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
