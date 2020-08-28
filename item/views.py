from django.contrib.auth.mixins import LoginRequiredMixin
import logging

from django.contrib import messages
from django.urls import reverse_lazy
from django.views import generic

from item.models import Item

from .forms import ItemCreateForm, ItemUpdateForm

logger = logging.getLogger(__name__)


class ItemCreateView(LoginRequiredMixin, generic.CreateView):
    """商品登録機能"""
    template_name = "item/item_create.html"
    model = Item
    form_class = ItemCreateForm
    success_url = reverse_lazy('item:item_list')

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
    """商品リストを表示"""
    template_name = 'item/item_list.html'
    model = Item
    paginate_by = 3

    def get_queryset(self):
        items = Item.objects.filter(user=self.request.user).order_by('pk')
        return items


class ItemDetailView(LoginRequiredMixin, generic.DetailView):
    """登録商品詳細表示"""
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
        print(form)
        messages.success(self.request, '商品詳細を更新しました。')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, '商品詳細の更新に失敗しました。')
        return super().form_invalid(form)


class ItemDeleteView(LoginRequiredMixin, generic.DeleteView):
    """商品削除機能"""
    template_name = 'item/item_delete.html'    # 削除確認画面
    model = Item
    success_url = reverse_lazy('item:item_list')

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, "商品を削除しました。")
        return super().delete(request, *args, **kwargs)


class OrderItemListView(LoginRequiredMixin, generic.ListView):

    template_name = 'item/order_item_list.html'
    model = Item
    success_url = reverse_lazy('order:index')
    paginate_by = 2

    def get_queryset(self):
        items = Item.objects.all().exclude(user=self.request.user).order_by('pk')
        return items
