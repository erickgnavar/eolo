from django import forms


class MeasurementFileForm(forms.Form):

    measurement_file = forms.FileField()
