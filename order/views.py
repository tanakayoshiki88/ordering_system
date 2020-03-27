from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
import logging

from django.contrib import messages
from django.urls import reverse_lazy
from django.views import generic

from .models import Item

from .forms import ContactForm, ItemCreateForm

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

class OderCreateView(LoginRequiredMixin, generic.CreateView):
    '''商品一覧 兼 注文画面'''
    template_name = "order/oder_create.html"
    model = Item




class ItemCreateView(LoginRequiredMixin, generic.CreateView):
    '''商品登録機能'''
    template_name = "order/item_create.html"
    model = Item
    form_class = ItemCreateForm
    success_url = reverse_lazy('order:item_create')

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
    paginate_by = 1

    def get_queryset(self):
        items = Item.objects.filter(user=self.request.user).order_by('created_at')
        return items
