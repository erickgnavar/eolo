from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.conf import settings
from django.core.urlresolvers import reverse

from common.views import LoginRequiredMixin

from weather.models import Filter
from weather.forms import FilterForm


class FilterListView(LoginRequiredMixin, ListView):

    model = Filter
    template_name = 'admin/filter/list.html'
    context_object_name = 'filters'
    paginate_by = settings.PAGE_SIZE


class FilterCreateView(LoginRequiredMixin, CreateView):

    model = Filter
    template_name = 'admin/filter/create.html'
    form_class = FilterForm

    def get_success_url(self):
        return reverse('admin_filter_list')


class FilterUpdateView(LoginRequiredMixin, UpdateView):

    model = filter
    template_name = 'admin/filter/edit.html'
    form_class = FilterForm

    def get_success_url(self):
        return reverse('admin_filter_list')


class FilterDeleteView(LoginRequiredMixin, DeleteView):

    model = Filter
    template_name = 'admin/filter/delete.html'

    def get_success_url(self):
        return reverse('admin_filter_list')
