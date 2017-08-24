import datetime
from django.test import TestCase
from model_mommy import mommy

from doctors.models import DoctorRecord, Doctor


class RecordDoctorTest(TestCase):
    def test_create_invalid_doctor_record(self):
        date_record = datetime.datetime.strptime('2017-08-23 21:36', "%Y-%m-%d %H:%M")
        with self.assertRaises(Exception) as context:
            mommy.make(DoctorRecord, date_record=date_record)
        self.assertTrue('Время записи с 09-00 до 17-00.' in context.exception)

    def test_create_exists_doctor_record(self):
        date_record = datetime.datetime.strptime('2017-08-23 14:00', "%Y-%m-%d %H:%M")
        doctor = Doctor.objects.create(fio="Петров Петр Петрович")
        record1 = mommy.make(DoctorRecord, date_record=date_record, doctor=doctor)
        with self.assertRaises(Exception) as context:
            record2 = mommy.make(DoctorRecord, date_record=date_record, doctor=doctor)
        self.assertTrue('Запись на это время к этому доктору уже сделана.' in context.exception)

    def test_create_valid_doctor_record(self):
        date_record = datetime.datetime.strptime('2017-08-25 14:00', "%Y-%m-%d %H:%M")
        record = mommy.make(DoctorRecord, date_record=date_record)
        self.assertTrue(isinstance(record, DoctorRecord))
        self.assertEqual(record.__str__(), "%s: %s" % (record.doctor.fio, record.date_record))
