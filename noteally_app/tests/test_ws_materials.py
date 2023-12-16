from rest_framework.test import APITestCase
from unittest import mock
from django.core.files import File
from django.urls import reverse
from noteally_app.tests.fill_db import fill_db
from rest_framework.exceptions import ErrorDetail
import shutil

# For Mocking Notifications
from unittest.mock import patch, MagicMock
from noteally_app.webservices.ws_materials import notify_subscribers

class TestMaterialsView(APITestCase):
    
    def setUp(self):
        self = fill_db(self)
        self.header = {'User-id': self.user1.id}
        self.url = reverse('materials')


    def tearDown(self):
        shutil.rmtree('test_media', ignore_errors=True)


    @patch('noteally_app.webservices.ws_materials.boto3')
    def test_post_material_success(self, mock_boto3):
        # mock response from boto3
        mock_boto3.client.return_value = MagicMock()

        file_mock = mock.MagicMock(spec=File, name="FileMock")
        file_mock.name = 'test.pdf'

        # Mock the part of the code that generates topic_name and topic_arn
        with patch('noteally_app.webservices.ws_materials.notify_subscribers') as mock_notify_subscribers:
            # form data
            data = {
                "user": self.user1.id,
                "name": "Introduction to Programming1",
                "description": "Introduction to Programming1",
                "price": 0,
                "university": self.university1.id,
                "file": file_mock,
                "study_areas": [self.study_area1.id, self.study_area2.id],
            }

            response = self.client.post(self.url, data, headers=self.header, format='multipart')
            
            expected_response = {
                "Success": "Successfully Created",
                "created_id": response.data['created_id'],
            }
            
            # Assert the response status code
            self.assertEqual(response.status_code, 201)
            
            # Assert the response data
            self.assertEqual(response.data['Success'], expected_response['Success'])
            
            # Assert that subscribe_to_sns_topic was called with the correct arguments
            mock_notify_subscribers.assert_called_once()

    def test_post_material_invalid_file(self):
        data = {
            "user": self.user1.id,
            "name": "Introduction to Programming2",
            "description": "Introduction to Programming2",
            "price": 0,
            "university": self.university1.id,
            "file": "string_instead_of_file",
            "study_areas": [self.study_area1.id, self.study_area2.id],
        }

        response = self.client.post(self.url, data, headers=self.header, format='multipart')
        
        expected_response = {
            'error': {
                'file': [ErrorDetail(string='The submitted data was not a file. Check the encoding type on the form.', code='invalid')]
                }
            }
        
        # Assert the response status code
        self.assertEqual(response.status_code, 400)
        
        # Assert the response data
        self.assertEqual(response.data, expected_response)
        
    @patch('noteally_app.webservices.ws_materials.boto3')
    def test_post_material_no_file(self, mock_boto3):
        # mock response from boto3
        mock_boto3.client.return_value = MagicMock()

        # Mock the part of the code that generates topic_name and topic_arn
        with patch('noteally_app.webservices.ws_materials.notify_subscribers') as mock_notify_subscribers:
            data = {
                "user": self.user1.id,
                "name": "Introduction to Programming3",
                "description": "Introduction to Programming3",
                "price": 0,
                "university": self.university1.id,
                "study_areas": [self.study_area1.id, self.study_area2.id],
            }
            
            response = self.client.post(self.url, data, headers=self.header, format='multipart')
            
            expected_response = {
                "Success": "Successfully Created",
                "created_id": response.data['created_id'],
            }
            
            # Assert the response status code
            self.assertEqual(response.status_code, 201)
            
            # Assert the response data
            self.assertEqual(response.data, expected_response)

            # Assert that subscribe_to_sns_topic was called with the correct arguments
            mock_notify_subscribers.assert_called_once()

    def test_get_materials_no_filter(self):
        response = self.client.get(self.url)

        # Assert the response status code
        self.assertEqual(response.status_code, 200)

        # Assert the response data
        self.assertEquals(len(response.data['results']), 2)

    
    def test_get_materials_match_1(self):
        data = {
            "name": "Calculus",
            "author": "John Doe",
            "study_areas": self.study_area2.id,
            "university": self.university2.id,
            "min_likes": 0,
            "min_downloads": 0,
            "max_price": 10,
            "order_by": "-total_downloads"
        }

        response = self.client.get(self.url, data)

        # Assert the response status code
        self.assertEqual(response.status_code, 200)

        # should exist 1 match
        self.assertEquals(len(response.data['results']), 1)

        # Assert the response data
        self.assertEquals(response.data['results'][0]['id'], self.material2.id)


    def test_get_materials_match_2(self):
        data = {
            "name": "Calculus",
            "author": "John",
            "study_areas": self.study_area2.id,
            "university": self.university2.id,
            "min_likes": 0,
            "min_downloads": 0,
            "free": "true",
            "order_by": "-total_downloads"
        }

        response = self.client.get(self.url, data)

        # Assert the response status code
        self.assertEqual(response.status_code, 200)

        # should exist 1 match
        self.assertEquals(len(response.data['results']), 1)

        # Assert the response data
        self.assertEquals(response.data['results'][0]['id'], self.material2.id)


    @patch('noteally_app.webservices.ws_materials.boto3.client')
    @patch('noteally_app.webservices.ws_materials.Response')  # Assuming Response is imported from DRF
    def test_notify_subscribers(self, mock_response, mock_boto3_client):
        # Mock the SNS client
        mock_sns_client = mock_boto3_client.return_value
        mock_sns_client.list_topics.return_value = {'Topics': []}
        mock_sns_client.publish.return_value = {'MessageId': 'test_message_id'}

        # Mock the serializer
        mock_serializer = MagicMock()
        mock_serializer.validated_data = {'name': 'Test Material'}

        # Mock the user
        mock_user = MagicMock()
        mock_user.id = 123
        mock_user.first_name = 'John'
        mock_user.last_name = 'Doe'

        with patch('builtins.print') as mock_print:
            # Call the function
            notify_subscribers(mock_serializer, mock_user)

            # Assert SNS client calls
            mock_sns_client.list_topics.assert_called_once()
            mock_sns_client.create_topic.assert_called_once_with(Name=f'uploads-user-{mock_user.id}')
            mock_sns_client.publish.assert_called_once_with(
                TopicArn=f'arn:aws:sns:{settings.AWS_REGION_NAME}:{settings.AWS_ACCOUNT_ID}:uploads-user-{mock_user.id}',
                Message=f"New material posted by {mock_user.first_name} {mock_user.last_name} with title {mock_serializer.validated_data['name']}",
                Subject=f"New material posted by {mock_user.first_name} {mock_user.last_name}",
                MessageStructure='string'
            )

            # Assert print calls
            mock_print.assert_any_call(f"Topic ARN: arn:aws:sns:{settings.AWS_REGION_NAME}:{settings.AWS_ACCOUNT_ID}:uploads-user-{mock_user.id}")
            mock_print.assert_any_call(f"Message: New material posted by {mock_user.first_name} {mock_user.last_name} with title {mock_serializer.validated_data['name']}")
            
            # Assert Response not called (since it's not an actual HTTP request)
            mock_response.assert_not_called()