from django.contrib.auth.mixins import LoginRequiredMixin
import logging

from django.contrib import messages
from django.urls import reverse_lazy
from django.views import generic

from item.models import Item

from .forms import ItemCreateForm, ItemUpdateForm

logger = logging.getLogger(__name__)


class ItemCreateView(LoginRequiredMixin, generic.CreateView):
    """販売商品登録機能"""
    template_name = "item/item_create.html"
    model = Item
    form_class = ItemCreateForm
    success_url = reverse_lazy('item:item_list')

    def form_valid(self, form):
        item = form.save(commit=False)
        item.user = self.request.user
        item.available_stock = item.stock  # フォームに入力された在庫数(stock)を有効在庫数としてavailable_stockへ挿入
        item.save()

        messages.success(self.request, '商品を登録しました。')

        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, '商品の登録に失敗しました。お手数ですが、はじめから登録をやり直してください。')

        return super().form_invalid(form)


class ItemListView(LoginRequiredMixin, generic.ListView):
    """登録商品一覧機能"""
    template_name = 'item/item_list.html'
    model = Item
    paginate_by = 3

    def get_queryset(self):
        items = Item.objects.filter(user=self.request.user).order_by('pk')
        return items


class ItemDetailView(generic.DetailView):
    """商品詳細表示機能"""
    template_name = 'item/item_detail.html'
    model = Item


class ItemUpdateView(LoginRequiredMixin, generic.UpdateView):
    """登録商品編集"""
    template_name = 'item/item_update.html'
    model = Item
    form_class = ItemUpdateForm

    def get_success_url(self):
        return reverse_lazy('item:item_detail', kwargs={'pk': self.kwargs['pk']})

    def form_valid(self, form):
        item = Item.objects.get(pk=self.object.pk)
        form_item = form.save(commit=False)
        form_item.user = self.request.user
        available_value = form_item.stock - item.reserved_stock
        form_item.available_stock = available_value  # フォームに入力された在庫数(stock)から引当在庫を引いて有効在庫数に入力

        item.save()

        messages.success(self.request, '商品詳細を更新しました。')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, '商品詳細の更新に失敗しました。')
        return super().form_invalid(form)


class ItemDeleteView(LoginRequiredMixin, generic.DeleteView):
    """登録商品削除機能"""
    template_name = 'item/item_delete.html'    # 削除確認画面
    model = Item
    success_url = reverse_lazy('item:item_list')

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, "商品を削除しました。")
        return super().delete(request, *args, **kwargs)


class OrderItemListView(generic.ListView):

    """購入商品一覧機能"""
    template_name = 'item/order_item_list.html'
    model = Item
    success_url = reverse_lazy('order:index')
    paginate_by = 2

    def get_queryset(self):
        # ログイン済み会なかで処理を分岐
        if self.request.user.is_authenticated:
            items = Item.objects.all().exclude(user=self.request.user).order_by('pk')
            return items
        else:
            items = Item.objects.all().order_by('pk')
            return items
