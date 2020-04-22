from django.contrib.auth.mixins import LoginRequiredMixin
import logging

from django.contrib import messages
from django.urls import reverse_lazy
from django.views import generic

from .models import Item, Order, FavoriteItem

from accounts.models import CustomUser

from .forms import ContactForm, ItemCreateForm, ItemUpdateForm, OrderCreateForm, OrderCreateFormSet, FavoriteItemCreateForm

logger = logging.getLogger(__name__)

# indexページの表示
class IndexView(generic.TemplateView):
    template_name = "order/index.html"

# お問い合わせフォームの表示
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


class ItemCreateView(LoginRequiredMixin, generic.CreateView):
    '''商品登録機能'''
    template_name = "order/item_create.html"
    model = Item
    form_class = ItemCreateForm
    success_url = reverse_lazy('order:item_list')

    def form_valid(self, form):
        item = form.save(commit=False)
        item.user = self.request.user
        item.save()

        messages.success(self.request, '商品を登録しました。')

        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, '商品の登録に失敗しました。お手数ですが、はじめから登録をやり直してください。')

        return super().form_invalid(form)

class ItemListView(LoginRequiredMixin, generic.ListView):
    '''商品リストを表示'''
    template_name = 'order/item_list.html'
    model = Item
    paginate_by = 10

    def get_queryset(self):
        items = Item.objects.filter(user=self.request.user).order_by('pk')
        return items

class ItemDetailView(LoginRequiredMixin, generic.DetailView):
    '''登録商品詳細表示'''
    template_name = 'order/item_detail.html'
    model = Item

class ItemUpdateView(LoginRequiredMixin, generic.UpdateView):
    '''登録商品編集'''
    template_name = 'order/item_update.html'
    model = Item
    form_class = ItemUpdateForm

    def get_success_url(self):
        return reverse_lazy('order:item_detail', kwargs={'pk': self.kwargs['pk']})

    def form_valid(self, form):
        messages.success(self.request, '商品詳細を更新しました。')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, '商品詳細の更新に失敗しました。')
        return super().form_invalid(form)

class ItemDeleteView(LoginRequiredMixin, generic.DeleteView):
    '''商品削除機能'''
    template_name = 'order/item_delete.html'    # 削除確認画面
    model = Item
    success_url = reverse_lazy('order:item_list')

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, "商品を削除しました。")
        return super().delete(request, *args, **kwargs)

class OrderCreateView(generic.CreateView):
    '''発注機能'''
    template_name = 'order/order_item_list.html'
    model = Order
    form_class = OrderCreateForm
    success_url = reverse_lazy('order:order_item_list')

    def form_valid(self, form):
        Order = form.save(commit=False)
        Order.user = self.request.user
        Order.save()

        messages.success(self.request, '商品を登録しました。')

        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, '商品の登録に失敗しました。お手数ですが、はじめから登録をやり直してください。')

        return super().form_invalid(form)


class OrderListView(generic.ListView):

    template_name = 'order/order_item_list.html'
    model = Item
    form_class = OrderCreateForm
    success_url = reverse_lazy('order:index')
    paginate_by = 2

    def get_queryset(self):
        items = Item.objects.all().order_by('pk')
        return items


class FavariteItemCreateView(generic.CreateView):
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
