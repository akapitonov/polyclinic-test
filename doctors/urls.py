from django.conf.urls import url, include

from doctors.wizards import DoctorRecordSessionWizard

urlpatterns = [
    url(r'^record/', DoctorRecordSessionWizard.as_view(), name='doctor-record'),
]