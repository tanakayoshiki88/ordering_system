from django.contrib.auth.mixins import LoginRequiredMixin
import logging

from django.contrib import messages
from django.urls import reverse_lazy
from django.views import generic

from order.models import Order
from item.models import Item

from .forms import ContactForm

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

'''
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
'''