from django.contrib import admin

from doctors.models import Doctor, DoctorRecord

admin.site.register(Doctor)
admin.site.register(DoctorRecord)
