from django.test import TestCase
from django.urls import reverse

from doctors.models import Doctor, DoctorRecord


class TestDoctorRecordSessionWizard(TestCase):
    wizard_url = reverse('doctor-record')
    wizard_steps_data = [
        {'doctor_record_session_wizard-current_step': 0
         },
        {
            'doctor_record_session_wizard-current_step': 1,
            '1-patient_fio': 'Александр',
            '1-date_record': '2017-08-25 13:00'
        }
    ]

    def test_initial_call(self):
        response = self.client.get(self.wizard_url)
        wizard = response.context['wizard']
        self.assertEqual(response.status_code, 200)
        self.assertEqual(wizard['steps'].current, '0')
        self.assertEqual(wizard['steps'].step0, 0)
        self.assertEqual(wizard['steps'].step1, 1)
        self.assertEqual(wizard['steps'].last, '1')
        self.assertEqual(wizard['steps'].prev, None)
        self.assertEqual(wizard['steps'].next, '1')
        self.assertEqual(wizard['steps'].count, 2)

    def _create_doctor(self, fio):
        doctor = Doctor.objects.get_or_create(fio=fio)
        if type(doctor) is tuple:
            doctor = doctor[0]
        self.assertTrue(isinstance(doctor, Doctor))
        return doctor

    def test_form_success_step0(self):
        doctor = self._create_doctor("Иванов Иван Иванович")
        self.wizard_steps_data[0]['0-doctor'] = doctor.pk
        response = self.client.post(self.wizard_url, self.wizard_steps_data[0])
        wizard = response.context['wizard']
        self.assertEqual(response.status_code, 200)
        self.assertEqual(wizard['steps'].current, '1')
        self.assertEqual(wizard['steps'].step0, 1)
        self.assertEqual(wizard['steps'].prev, '0')
        self.assertEqual(wizard['steps'].next, None)

    def test_form_full_fill(self):
        doctor = self._create_doctor("Петров Петр Петрович")
        self.wizard_steps_data[0]['0-doctor'] = doctor.pk
        response = self.client.post(self.wizard_url, self.wizard_steps_data[0])
        wizard = response.context['wizard']
        self.assertEqual(response.status_code, 200)
        self.assertEqual(wizard['steps'].current, '1')
        records = DoctorRecord.get_invalid_date_record(doctor)
        self.wizard_steps_data[1]['records'] = records
        response = self.client.post(self.wizard_url, self.wizard_steps_data[1])
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'успешно записались')

    def test_form_full_fill_invalid(self):
        self.test_form_full_fill()
        doctor = self._create_doctor("Петров Петр Петрович")
        self.wizard_steps_data[0]['0-doctor'] = doctor.pk
        response = self.client.post(self.wizard_url, self.wizard_steps_data[0])
        wizard = response.context['wizard']
        self.assertEqual(response.status_code, 200)
        self.assertEqual(wizard['steps'].current, '1')
        records = DoctorRecord.get_invalid_date_record(doctor)
        self.wizard_steps_data[1]['records'] = records
        response = self.client.post(self.wizard_url, self.wizard_steps_data[1])
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'возникли ошибки')


