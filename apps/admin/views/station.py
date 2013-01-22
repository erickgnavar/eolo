from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.conf import settings
from django.core.urlresolvers import reverse

from common.views import LoginRequiredMixin

from weather.models import Station
from weather.forms import StationForm


class StationListView(LoginRequiredMixin, ListView):

    model = Station
    template_name = 'admin/station/list.html'
    context_object_name = 'stations'
    paginate_by = settings.PAGE_SIZE


class StationCreateView(LoginRequiredMixin, CreateView):

    model = Station
    template_name = 'admin/station/create.html'
    form_class = StationForm

    def get_success_url(self):
        return reverse('admin_station_list')


class StationUpdateView(LoginRequiredMixin, UpdateView):

    model = Station
    template_name = 'admin/station/edit.html'
    form_class = StationForm

    def get_success_url(self):
        return reverse('admin_station_list')


class StationDeleteView(LoginRequiredMixin, DeleteView):

    model = Station
    template_name = 'admin/station/delete.html'

    def get_success_url(self):
        return reverse('admin_station_list')
