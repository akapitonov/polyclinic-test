from django.test import TestCase

from django.urls import reverse


class CottageViewTest(TestCase):
    def test_doctor_record_view(self):
        url = reverse('doctor-record')
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)

    def test_home_view(self):
        url = reverse('base')
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)