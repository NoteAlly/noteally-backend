from rest_framework.test import APITestCase
from django.urls import reverse
from noteally_app.models import StudyArea, University


class TestMaterialsView(APITestCase):
    
    def setUp(self):
        # Study areas
        self.study_area1 = StudyArea.objects.create(name="Computer Science")
        self.study_area2 = StudyArea.objects.create(name="Mathematics")
        self.study_area3 = StudyArea.objects.create(name="Physics")
        self.study_area4 = StudyArea.objects.create(name="Chemistry")
        self.study_area5 = StudyArea.objects.create(name="Biology")

        # Universities
        self.university1 = University.objects.create(name="University of Aveiro")
        self.university2 = University.objects.create(name="University of Lisboa")
        self.url = reverse('info')


    def test_get_info(self):
        response = self.client.get(self.url)

        # Assert the response status code
        self.assertEqual(response.status_code, 200)

        # Assert the response data
        self.assertEquals(len(response.data['universities']), 2)
        self.assertEquals(len(response.data['study_areas']), 5)
