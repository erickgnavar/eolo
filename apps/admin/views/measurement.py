from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.conf import settings
from django.core.urlresolvers import reverse

from common.views import LoginRequiredMixin

from weather.models import Measurement
from weather.forms import MeasurementForm, MeasurementSearchForm


class MeasurementListView(LoginRequiredMixin, ListView):

    model = Measurement
    template_name = 'admin/measurement/list.html'
    context_object_name = 'measurements'
    paginate_by = settings.PAGE_SIZE

    def get_context_data(self, **kwargs):
        context = super(MeasurementListView, self).get_context_data(**kwargs)
        if len(self.request.GET) > 0:
            context['search_form'] = MeasurementSearchForm(self.request.GET)
        else:
            context['search_form'] = MeasurementSearchForm()

        return context

    def get_queryset(self):
        qs = super(MeasurementListView, self).get_queryset()
        variable = self.request.GET.get('variable', '')
        if len(variable) > 0:
            qs = qs.filter(variable=variable)
        date = self.request.GET.get('date', '')
        if len(date) > 0:
            qs = qs.filter(date=date)
        return qs


class MeasurementCreateView(LoginRequiredMixin, CreateView):

    model = Measurement
    template_name = 'admin/measurement/create.html'
    form_class = MeasurementForm

    def get_success_url(self):
        return reverse('admin_measurement_list')


class MeasurementUpdateView(LoginRequiredMixin, UpdateView):

    model = Measurement
    template_name = 'admin/measurement/edit.html'
    form_class = MeasurementForm

    def get_success_url(self):
        return reverse('admin_measurement_list')


class MeasurementDeleteView(LoginRequiredMixin, DeleteView):

    model = Measurement
    template_name = 'admin/measurement/delete.html'

    def get_success_url(self):
        return reverse('admin_measurement_list')
