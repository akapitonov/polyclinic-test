from django.core.exceptions import ValidationError
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from formtools.wizard.views import SessionWizardView

from doctors.forms import ChooseDoctorForm, ChooseDateRecordForm
from doctors.models import DoctorRecord


class DoctorRecordSessionWizard(SessionWizardView):
    form_list = [ChooseDoctorForm, ChooseDateRecordForm]
    template_name = 'doctors/wizard_record.html'

    def get_context_data(self, form, **kwargs):
        ctx = super(DoctorRecordSessionWizard, self).get_context_data(form, **kwargs)
        if self.steps.index == 1:
            data_step0 = self.get_cleaned_data_for_step('0')
            if data_step0:
                doctor = data_step0.get('doctor', None)
                records = DoctorRecord.get_valid_dates_record(doctor)
                ctx['records'] = records
        return ctx

    def done(self, form_list, **kwargs):
        form_data = {}
        for form in form_list:
            form_data.update(form.cleaned_data)

        try:
            record = DoctorRecord.objects.create(**form_data)
        except ValidationError as e:
            record = None
            errors = e.messages
        if record:
            return render(self.request, 'doctors/wizard_success.html', {'record': record})
        elif record is None:
            return render(self.request, 'doctors/wizard_errors.html', {'errors': errors})
        return HttpResponseRedirect(reverse('doctor-record'))
