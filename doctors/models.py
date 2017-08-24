import datetime
import json

from django.core.exceptions import ValidationError
from django.db import models
from .times import AVAILABLE_TIMES
from django.utils.translation import gettext_lazy as _


class Doctor(models.Model):
    fio = models.CharField(_('doctor_fio'), max_length=150)

    class Meta:
        verbose_name = _('doctor_verbose_name')
        verbose_name_plural = _('doctor_verbose_name_plural')

    def __str__(self):
        return self.fio


class DoctorRecord(models.Model):
    doctor = models.ForeignKey(Doctor, verbose_name=_('doctor_fio'))
    patient_fio = models.CharField(_('patient_fio'), max_length=150)
    date_record = models.DateTimeField(_('date_record'))

    class Meta:
        verbose_name = _('record_verbose_name')
        verbose_name_plural = _('record_verbose_name_plural')

    def save(self, *args, **kwargs):
        try:
            self.full_clean()
        except ValidationError as e:
            raise ValidationError(e.messages)
        super(DoctorRecord, self).save(*args, **kwargs)

    def _check_exist(self):
        doctor = getattr(self, 'doctor', None)
        if doctor:
            return DoctorRecord.objects.filter(doctor=self.doctor, date_record=self.date_record).exists()
        return False

    def clean(self):
        if self.date_record:
            hour = self.date_record.hour
            minute = self.date_record.minute
            if hour > 17 or hour < 9 or minute != 0:
                raise ValidationError(_('error_record_time_range'))
            elif self._check_exist():
                raise ValidationError(_('error_record_time_occupied'))

    def __str__(self):
        return "%s: %s" % (self.doctor, self.date_record)


    @staticmethod
    def _get_times_for_today(today, occupied=None):
        hour = today.hour
        today_times = []
        for index, time in enumerate(AVAILABLE_TIMES):
            if occupied is None or time not in occupied:
                try:
                    time_hour = int(time.split('-')[0])
                except ValueError:
                    time_hour = -1

                if time_hour >= hour:
                    today_times.append(time)
        return today_times

    @classmethod
    def _get_invalid_doctor_date_record(cls, doctor):
        """
        кто записался на прием к доктору
        на время больше чем сейчас
        :param doctor: доктор
        :return: список занятого времени
        """
        new_dates = {}
        today = datetime.datetime.today()
        occupied_dates = cls.objects.filter(date_record__gte=today,
                                            doctor=doctor).values_list('date_record', flat=True).order_by('date_record')
        for date in occupied_dates:
            only_date = date.strftime('%Y-%m-%d')
            if only_date in new_dates:
                val = new_dates[only_date]
                if val is None:
                    new_dates[only_date] = [date.strftime('%H-00')]
                else:
                    new_dates[only_date].append(date.strftime('%H-00'))
            else:
                new_dates[only_date] = [date.strftime('%H-00')]
        return new_dates

    @classmethod
    def get_valid_dates_record(cls, doctor):
        if doctor:
            new_dates = {}
            today = datetime.datetime.today()
            occupied_dates = cls._get_invalid_doctor_date_record(doctor)

            for date, times in occupied_dates.items():
                new_dates[date] = [time for time in AVAILABLE_TIMES if time not in times]

            today_format = today.strftime('%Y-%m-%d')
            if today_format in new_dates:
                new_dates[today_format] = cls._get_times_for_today(today, new_dates[today_format])
            else:
                new_dates[today_format] = cls._get_times_for_today(today)

            new_dates.update({"all": AVAILABLE_TIMES})

            return json.dumps(new_dates)
        return None
