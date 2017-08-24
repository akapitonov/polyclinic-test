from django import forms

from doctors.models import DoctorRecord


class ChooseDoctorForm(forms.ModelForm):
    class Meta:
        model = DoctorRecord
        fields = ['doctor']


class ChooseDateRecordForm(forms.ModelForm):
    class Meta:
        model = DoctorRecord
        fields = ['patient_fio', 'date_record']


