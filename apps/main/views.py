from datetime import timedelta

from django.views.generic.edit import FormView
from django.views.generic import TemplateView
from django.shortcuts import render_to_response
from django.template import RequestContext

from main.forms import ConsultForm
from weather.models import Measurement
# from common.util import Stadistical
from decimal import Decimal


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
        # remove
        # print Stadistical.mode(values), Stadistical.median(values)
        context = {
            # 'average': Stadistical.average(values),
            # 'mode': Stadistical.mode(values),
            # 'median': Stadistical.median(values),
            'measurements': Measurement.objects.filter(id__in=ids).order_by('date'),
            'data': prepare_data(values),
            'variable': variable
        }
        params = ('main/report.html', context, RequestContext(self.request))
        prepare_data(values)
        return render_to_response(*params)


class ReportView(TemplateView):

    template_name = 'main/report.html'


def prepare_data(values):
    import math
    length = len(values)
    quantity = int(round(1 + (3.3 * math.log(length))))
    amplitude = (max(values) - min(values)) / Decimal(quantity)
    limit_decimal = 5
    data = {
        'length': length,
        'intervals': [],
        'amplitude': round(amplitude, limit_decimal)
    }
    m = min(values)
    for i in range(quantity):
        interval = {
            'index': 0,
            'min': round(m, limit_decimal),
            'max': round(m + amplitude, limit_decimal),
            'values': []
        }
        data['intervals'].append(interval)
        m += amplitude
    # insert first data
    min_value = min(values)
    for i in range(values.count(min_value)):
        data['intervals'][0]['values'].append(min_value)
    # insert rest data
    for value in values:
        for interval in data['intervals']:
            if value > interval['min'] and value <= interval['max']:
                interval['values'].append(value)
    count = 0
    for interval in data['intervals']:
        count += 1
        interval['index'] = count
        interval['class_marker'] = (interval['max'] + interval['min']) / 2
        interval['fi'] = len(interval['values'])
        interval['hi'] = round(float(interval['fi']) / float(data['length']), limit_decimal)
        interval['Fi'] = 0
        interval['Hi'] = 0

    data['intervals'][0]['Fi'] = data['intervals'][0]['fi']
    data['intervals'][0]['Hi'] = round(data['intervals'][0]['hi'], limit_decimal)
    for i in range(1, quantity):
        data['intervals'][i]['Fi'] += data['intervals'][i - 1]['Fi'] + data['intervals'][i]['fi']
        data['intervals'][i]['Hi'] += round(data['intervals'][i - 1]['Hi'] + data['intervals'][i]['hi'], limit_decimal)

    a = 0
    modal_class_index = 0
    b = 0
    for interval in data['intervals']:
        a += interval['fi'] * interval['class_marker']
        if interval['fi'] > b:
            b = interval['fi']
            modal_class_index = interval['index'] - 1
    # Median
    median = data['intervals'][modal_class_index]['min']
    if modal_class_index == 0:
        before_value = data['intervals'][0]['Fi']
    else:
        before_value = data['intervals'][modal_class_index - 1]['Fi']

    median += (((data['length'] / 2) - before_value) / data['intervals'][modal_class_index]['class_marker']) * float(data['amplitude'])
    # Median end
    data['median'] = round(median, limit_decimal)
    # Mode

    # Mode end
    # Average
    data['average'] = round(a / length, limit_decimal)

    if modal_class_index - 1 <= 0:
        x = data['intervals'][modal_class_index]['fi'] - float(data['intervals'][modal_class_index]['min'])
    else:
        x = data['intervals'][modal_class_index]['fi'] - float(data['intervals'][modal_class_index - 1]['fi'])
    if modal_class_index + 1 >= data['length']:
        y = data['intervals'][modal_class_index]['fi'] - float(data['intervals'][modal_class_index]['max'])
    else:
        y = data['intervals'][modal_class_index]['fi'] - float(data['intervals'][modal_class_index + 1]['fi'])
    mode = data['intervals'][modal_class_index]['min'] + ((x / (x + y)) * float(data['amplitude']))

    data['mode'] = round(mode, limit_decimal)

    return data
