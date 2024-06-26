from django.contrib.auth.mixins import LoginRequiredMixin
import logging
from django.shortcuts import render, redirect
from django.core.exceptions import ObjectDoesNotExist
from django.core.mail import send_mail

from django.contrib import messages
from django.urls import reverse_lazy
from django.views import generic

from order.models import Order
from cart.models import CartItem
from item.models import Item

from .forms import ContactForm, OrderUpdateFormSetBySeller

import os
import math

logger = logging.getLogger(__name__)

__tax_rate__ = 1.1


# indexページの表示
class IndexView(generic.TemplateView):
    template_name = "order/index.html"


# お問い合わせ機能
class ContactView(generic.FormView):
    template_name = "order/contact.html"
    form_class = ContactForm
    success_url = reverse_lazy('order:contact')

    def form_valid(self, form):
        name = form.cleaned_data['last_name'] + " " + form.cleaned_data['first_name']

        form.send_email()
        messages.success(self.request, 'メッセージを送信しました!!')
        logger.info('contact send by {}'.format('name'))

        return super().form_valid(form)


# 発注商品リストを表示
class PlacedOrderListView(LoginRequiredMixin, generic.ListView):
    template_name = 'order/placed_order_list.html'
    model = Order
    paginate_by = 5

    def get_queryset(self):
        order_items = Order.objects.filter(buyer=self.request.user).order_by('-pk')
        return order_items


def order_confirm(request, total=0, counter=0, cart_items=None):
    try:
        cart_items = CartItem.objects.filter(buyer=request.user, is_active=True).order_by('pk')
        warning_msg = {}
        for cart_item in cart_items:
            if cart_item.item.stock > 0:
                if cart_item.item.stock > cart_item.quantity:
                    if cart_item.item.including_tax:
                        total += math.floor(cart_item.item.price * cart_item.quantity)
                    else:
                        total += math.floor(cart_item.item.price * cart_item.quantity * __tax_rate__)
                else:
                    if cart_item.item.including_tax:
                        total += math.floor(cart_item.item.price * cart_item.quantity)
                    else:
                        total += math.floor(cart_item.item.price * cart_item.quantity * __tax_rate__)
                    warning_msg[cart_item.item_id] = 'こちらの商品は現在、在庫数が' + str(cart_item.item.stock) + cart_item.item.unit + 'です。'
            else:
                if cart_item.item.including_tax:
                    total += math.floor(cart_item.item.price * cart_item.quantity)
                else:
                    total += math.floor(cart_item.item.price * cart_item.quantity * __tax_rate__)
                warning_msg[cart_item.item_id] = 'こちらの商品は現在、在庫数がありません。'
    except ObjectDoesNotExist:
        pass
    return render(request, 'order_confirm.html', dict(cart_items=cart_items, total=total, warning_msg=warning_msg))


def order_create(request):

    all_items_total_price = 0
    item_name_quantity_for_sending_email = {}
    counter = 0

    try:
        cart_items = CartItem.objects.filter(buyer=request.user, is_active=True).order_by('-pk')
        # Orderモデルインスタンス作成
        for cart_item in cart_items:
            if cart_item.quantity != 0 and cart_item.quantity <= cart_item.item.stock:
                # Itemモデルのstock（在庫数）フィールドを発注分減らし、is_activeフィールドをFalseに更新
                item = Item.objects.get(pk=cart_item.item.id)
                item.stock -= cart_item.quantity
                cart_item.is_active = False

                item.save()

                if cart_item.item.including_tax:
                    total_price = (cart_item.item.price * cart_item.quantity)
                    total_unit = cart_item.quantity
                    all_items_total_price += total_price
                else:
                    total_price = (cart_item.item.price * cart_item.quantity * __tax_rate__)
                    total_unit = cart_item.quantity
                    all_items_total_price += total_price

                item_name_quantity_for_sending_email[cart_item.item.name] = str(cart_item.quantity) + cart_item.item.unit

                order = Order.objects.create(
                    buyer=request.user,
                    seller=cart_item.item.user,
                    item_id=cart_item.item.pk,
                    name=cart_item.item.name,
                    price=cart_item.item.price,
                    including_tax=cart_item.item.including_tax,
                    quantity=cart_item.quantity,
                    unit=cart_item.item.unit,
                    moq=cart_item.item.moq,
                    spq=cart_item.item.spq,
                    photo=cart_item.item.photo,
                    total_unit=total_unit,
                    total_price=total_price,
                )
                order.save()
                cart_item.quantity = 0
                cart_item.save()
                counter += 1

    except ObjectDoesNotExist:
        pass

    if counter > 0:
        messages.success(request, '発注が完了しました。詳細は発注履歴一覧でご覧いただけます。')

        try:
            # 発注情報メール件名
            subject = "Juhatchu 発注情報"
            # 受注情報メールメッセージ
            message_for_seller = str(request.user)\
                + "様から発注がありました。\n詳細は、受注一覧より確認いただけます。\n"\
                + "----------------------------------------\n"\
                + str("\n"
                      .join(["{0} - {1}"
                            .format(key, value) for (key, value) in item_name_quantity_for_sending_email.items()]))
            # 受注情報メールメッセージfor DEFAULT_FROM_EMAIL
            message_for_from = str(request.user) \
                      + "様から発注がありました。\n詳細は、受注一覧より確認いただけます。\n" \
                      + "----------------------------------------\n" \
                      + str("\n"
                            .join(["{0} - {1}"
                                  .format(key, value) for (key, value) in item_name_quantity_for_sending_email.items()]))

            # 送信元アドレス
            from_email = os.environ.get('DEFAULT_FROM_EMAIL')
            # 送信先アドレス
            seller = cart_item.item.user.email
            recipient_list_for_seller = [seller]
            recipient_list_for_from = [os.environ.get('DEFAULT_FROM_EMAIL')]
            # メール送信
            send_mail(subject, message_for_seller, from_email, recipient_list_for_seller)
            send_mail(subject, message_for_from, from_email, recipient_list_for_from)
        except ObjectDoesNotExist:
            pass

        return redirect('order:placed_order_list')

    return redirect('cart:cart_detail')


def received_order_list(request):

    if request.user.is_anonymous:
        return redirect('account_login')
    else:
        formset = OrderUpdateFormSetBySeller(
            request.POST or None, queryset=Order.objects.filter(seller=request.user)
        )
        order_list = Order.objects.filter(seller=request.user)

        if request.method == 'POST' and formset.is_valid():
            formset.save()
            return redirect('order:received_order_list')

        context = {
            'formset': formset,
            'order_list': order_list,
        }

        return render(request, 'order/received_order_list.html', context)


"""
class FavoriteItemCreateView(generic.CreateView):
    template_name = 'order/favorite_item_create.html'
    model = FavoriteItem
    form_class = FavoriteItemCreateForm
    success_url = reverse_lazy('order:index')

    def get_form_kwargs(self, *args, **kwargs):
        form_kwargs = super().get_form_kwargs(*args, **kwargs)
        form_kwargs['initial'] = {'user': self.request.user, 'item': self.kwargs.get('pk')}  # フォームに初期値を設定する。
        print(self.request)
        print(self.args)
        print(self.kwargs)
        print(self.kwargs.get('pk'))
        print(self.kwargs.get('name'))
        print(form_kwargs)
        return form_kwargs

    def form_valid(self, form):
        FavoriteItem = form.save(commit=False)
        FavoriteItem.user = self.request.user
        FavoriteItem.item = self.kwargs.get('pk')

        FavoriteItem.save()

        messages.success(self.request, '商品を登録しました。')

        return super().form_valid(form)
"""