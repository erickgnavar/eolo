from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.conf import settings
from django.core.urlresolvers import reverse

from common.views import LoginRequiredMixin

from weather.models import Region
from weather.forms import RegionForm


class RegionListView(LoginRequiredMixin, ListView):

    model = Region
    template_name = 'admin/region/list.html'
    context_object_name = 'regions'
    paginate_by = settings.PAGE_SIZE


class RegionCreateView(LoginRequiredMixin, CreateView):

    model = Region
    template_name = 'admin/region/create.html'
    form_class = RegionForm

    def get_success_url(self):
        return reverse('admin_region_list')


class RegionUpdateView(LoginRequiredMixin, UpdateView):

    model = Region
    template_name = 'admin/region/edit.html'
    form_class = RegionForm

    def get_success_url(self):
        return reverse('admin_region_list')


class RegionDeleteView(LoginRequiredMixin, DeleteView):

    model = Region
    template_name = 'admin/region/delete.html'

    def get_success_url(self):
        return reverse('admin_region_list')
