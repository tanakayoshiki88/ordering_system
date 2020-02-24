import logging

from django.contrib import messages
from django.urls import reverse_lazy
from django.views import generic

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
