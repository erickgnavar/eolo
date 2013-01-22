from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.conf import settings
from django.core.urlresolvers import reverse

from common.views import LoginRequiredMixin

from weather.models import Variable
from weather.forms import VariableForm


class VariableListView(LoginRequiredMixin, ListView):

    model = Variable
    template_name = 'admin/variable/list.html'
    context_object_name = 'variables'
    paginate_by = settings.PAGE_SIZE


class VariableCreateView(LoginRequiredMixin, CreateView):

    model = Variable
    template_name = 'admin/variable/create.html'
    form_class = VariableForm

    def get_success_url(self):
        return reverse('admin_variable_list')


class VariableUpdateView(LoginRequiredMixin, UpdateView):

    model = Variable
    template_name = 'admin/variable/edit.html'
    form_class = VariableForm

    def get_success_url(self):
        return reverse('admin_variable_list')


class VariableDeleteView(LoginRequiredMixin, DeleteView):

    model = Variable
    template_name = 'admin/variable/delete.html'

    def get_success_url(self):
        return reverse('admin_variable_list')
