from django import forms

from weather.models import Variable, Measurement, Region, Station, Filter


class VariableForm(forms.ModelForm):

    class Meta:
        model = Variable


class MeasurementForm(forms.ModelForm):

    class Meta:
        model = Measurement

    def __init__(self, *args, **kwargs):
        super(MeasurementForm, self).__init__(*args, **kwargs)
        self.fields['date'].widget.attrs['class'] = 'datepicker'


class MeasurementSearchForm(forms.Form):

    variable = forms.ModelChoiceField(
        required=False,
        queryset=Variable.objects.all()
    )
    date = forms.DateField(
        required=False
    )

    def __init__(self, *args, **kwargs):
        super(MeasurementSearchForm, self).__init__(*args, **kwargs)
        self.fields['date'].widget.attrs['class'] = 'datepicker'


class RegionForm(forms.ModelForm):

    class Meta:
        model = Region


class StationForm(forms.ModelForm):

    class Meta:
        model = Station


class FilterForm(forms.ModelForm):

    class Meta:
        model = Filter
