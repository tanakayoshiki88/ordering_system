from django.views import generic

from .forms import InquiryForm

class IndexView(generic.TemplateView):
    template_name = "order/index.html"


class InquiryView(generic.FormView):
    template_name = "order/inquiry.html"
    form_class = InquiryForm
