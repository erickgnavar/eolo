from datetime import timedelta

from django.views.generic.edit import FormView
from django.views.generic import TemplateView
from django.shortcuts import render_to_response
from django.template import RequestContext

from main.forms import ConsultForm
from weather.models import Measurement


class HomeView(FormView):

    template_name = 'main/home.html'
    form_class = ConsultForm

    def form_valid(self, form):
        data = form.cleaned_data
        date = data['date']
        length = data['length']
        variable = data['variable']
        qs = Measurement.objects.filter(variable=variable).exclude(value=None)
        values = []
        ids = []
        # values before date selected
        for delta in range(-length, 0):
            delta_date = date + timedelta(days=delta)
            filters = {
                'date__day': delta_date.day,
                'date__month': delta_date.month,
                'date__lte': date
            }
            values += [measurement.value for measurement in qs.filter(**filters)]
            ids += [measurement.id for measurement in qs.filter(**filters)]
        # values for date selecte before one year
        filters = {
            'date__day': date.day,
            'date__month': date.month,
            'date__lt': date + timedelta(days=-365)
        }
        values += [measurement.value for measurement in qs.filter(**filters)]
        ids += [measurement.id for measurement in qs.filter(**filters)]
        # values above date selected
        for delta in range(1, length + 1):
            delta_date = date + timedelta(days=delta)
            filters = {
                'date__day': delta_date.day,
                'date__month': delta_date.month,
                'date__lte': date
            }
            values += [measurement.value for measurement in qs.filter(**filters)]
            ids += [measurement.id for measurement in qs.filter(**filters)]
        values.sort()
        ids.sort()
        context = {
            'average': reduce(lambda x, y: x + y, values) / len(values),
            'measurements': Measurement.objects.filter(id__in=ids)
        }
        params = ('main/report.html', context, RequestContext(self.request))
        return render_to_response(*params)


class ReportView(TemplateView):

    template_name = 'main/report.html'
