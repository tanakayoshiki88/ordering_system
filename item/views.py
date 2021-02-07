from django.contrib.auth.mixins import LoginRequiredMixin
import logging

from django.contrib import messages
from django.urls import reverse_lazy
from django.views import generic

from item.models import Item
from django.db.models import Q

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
    paginate_by = 2

    def get_queryset(self):
        # ログイン済み会なかで処理を分岐
        if self.request.user.is_authenticated:
            items = Item.objects.all().exclude(user=self.request.user).order_by('pk')
            return items
        else:
            items = Item.objects.all().order_by('pk')
            return items


class SearchItemListView(generic.ListView):
    """商品検索結果表示"""
    template_name = 'item/search_item_list.html'
    model = Item
    paginate_by = 3


    def get_queryset(self):
        # ログイン済みか否かで処理を分岐
        if self.request.user.is_authenticated:
            # ログイン済み
            query = self.request.GET.get('query')
            select_item = self.request.GET.get('select-item')


            # select_itemがpurchase-itemかsales-itemかで分岐
            if select_item == 'purchase-items':

                # 購入商品検索(purchase-item)
                items = Item.objects.filter(
                    Q(name__icontains=query)
                    | Q(item_description__icontains=query)
                    | Q(category1__icontains=query)
                    | Q(category2__icontains=query)
                    | Q(category3__icontains=query)
                ).exclude(user=self.request.user).order_by('pk')

                # 検索結果件数
                count = Item.objects.filter(
                    Q(name__icontains=query)
                    | Q(item_description__icontains=query)
                    | Q(category1__icontains=query)
                    | Q(category2__icontains=query)
                    | Q(category3__icontains=query)
                ).exclude(user=self.request.user).order_by('pk').count()

                messages.success(self.request, query + 'を含む検索結果：' + str(count) + '件')

            else:

                # 販売商品検索(sales-item)
                items = Item.objects.filter(
                    Q(name__icontains=query)
                    | Q(item_description__icontains=query)
                    | Q(category1__icontains=query)
                    | Q(category2__icontains=query)
                    | Q(category3__icontains=query)
                ).filter(user=self.request.user).order_by('pk')

                # 検索結果件数
                count = Item.objects.filter(
                    Q(name__icontains=query)
                    | Q(item_description__icontains=query)
                    | Q(category1__icontains=query)
                    | Q(category2__icontains=query)
                    | Q(category3__icontains=query)
                ).filter(user=self.request.user).order_by('pk').count()

                messages.success(self.request, query + 'を含む検索結果：' + str(count) + '件')

            return items

        else:
            # ログイン未済
            query = self.request.GET.get('query')

            # 販売登録されたすべての商品を取得
            items = Item.objects.filter(
                Q(name__icontains=query)
                | Q(item_description__icontains=query)
                | Q(category1__icontains=query)
                | Q(category2__icontains=query)
                | Q(category3__icontains=query)
            ).order_by('pk')

            # レコード件数を取得
            count = Item.objects.filter(
                Q(name__icontains=query)
                | Q(item_description__icontains=query)
                | Q(category1__icontains=query)
                | Q(category2__icontains=query)
                | Q(category3__icontains=query)
            ).order_by('pk').count()

            messages.success(self.request, query + 'を含む検索結果：' + str(count) + '件')

        return items
