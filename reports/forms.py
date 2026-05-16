from django import forms
from .models import Report

class ReportForm(forms.ModelForm):
    class Meta:
        model = Report
        fields = [
            'reported_status',
            'full_address',
            'pole_image',
            'pole_number_image',
            'reported_status',
            ]