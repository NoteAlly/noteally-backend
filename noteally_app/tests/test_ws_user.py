from rest_framework.test import APITestCase
from django.urls import reverse
from noteally_app.tests.fill_db import fill_db
from django.db.models import Max
from noteally_app.models import User, Follower
from django.conf import settings

# To mock the SNS topic creation
from unittest.mock import patch, MagicMock
from noteally_app.webservices.ws_user import subscribe_to_sns_topic

# import ErrorDetail in the line below
from rest_framework.exceptions import ErrorDetail


class TestUserView(APITestCase):
    
    def setUp(self):
        self = fill_db(self)
        
    def test_unlock_premium(self):
        assert self.user2.premium == False
        
        url = reverse('unlock_premium')
        headers = {'User-id': self.user2.id}
        
        response = self.client.post(url, headers=headers)
        
        expected_response = {
            'user_id': self.user2.id,
            'message': 'Premium unlocked'
        }
        
        # Assert the response status code
        self.assertEqual(response.status_code, 200)
        
        # Assert the response data
        self.assertEqual(response.data, expected_response)
    
    
    def test_unlock_premium_already_premium(self):
        assert self.user1.premium == True
        
        url = reverse('unlock_premium')
        headers = {'User-id': self.user1.id}
        
        response = self.client.post(url, headers=headers)
        
        expected_response = {
            'error': 'User is already premium'
        }
        
        # Assert the response status code
        self.assertEqual(response.status_code, 400)
        
        # Assert the response data
        self.assertEqual(response.data, expected_response)
        
    
    def test_unlock_premium_invalid_id(self):
        max_id = User.objects.aggregate(max_id=Max('id'))['max_id']
        non_existent_id = max_id + 1 if max_id is not None else 1
        
        url = reverse('unlock_premium')
        headers = {'User-id': non_existent_id}
        
        response = self.client.post(url, headers=headers)
        
        expected_response = {
            'error': 'User not found'
        }
        
        # Assert the response status code
        self.assertEqual(response.status_code, 400)
        
        # Assert the response data
        self.assertEqual(response.data, expected_response)
        
    
    def test_unlock_premium_no_id(self):
        url = reverse('unlock_premium')
        
        response = self.client.post(url)
        
        expected_response = {
            'error': 'User-id header not found'
        }
        
        # Assert the response status code
        self.assertEqual(response.status_code, 400)
        
        # Assert the response data
        self.assertEqual(response.data, expected_response)
    
    
    def test_unlock_premium_get_method(self):
        url = reverse('unlock_premium')
        headers = {'User-id': self.user1.id}
        
        response = self.client.get(url, headers=headers)
        
        expected_response = {
            'detail': ErrorDetail(string='Method "GET" not allowed.', code='method_not_allowed')
        }
           
        # Assert the response status code
        self.assertEqual(response.status_code, 405)
        
        # Assert the response data
        self.assertEqual(response.data, expected_response)
        
    @patch('noteally_app.webservices.ws_user.boto3')
    def test_subscribe(self, mock_boto3):
        # mock response from boto3
        mock_boto3.client.return_value = MagicMock()
        
        # Mock the part of the code that generates topic_name and topic_arn
        with patch('noteally_app.webservices.ws_user.subscribe_to_sns_topic') as mock_subscribe_to_sns_topic:
            # Assuming self.user1 and self.user2 are defined earlier in your test setup
            url = reverse('subscribe', args=[self.user1.id])
            headers = {'User-id': self.user2.id}

            response = self.client.post(url, headers=headers)

            expected_response = {
                'message': 'Successfully subscribed'
            }

            # Assert the response status code
            self.assertEqual(response.status_code, 201)

            # Assert the response data
            self.assertEqual(response.data, expected_response)

            # Assert that subscribe_to_sns_topic was called with the correct arguments
            mock_subscribe_to_sns_topic.assert_called_once_with(self.user2, self.user1)

    def test_unsubscribe(self):
        # Assuming self.user2 is already subscribed to self.user1
        Follower.objects.create(follower=self.user2, following=self.user1)

        url = reverse('unsubscribe', args=[self.user1.id])
        headers = {'User-id': self.user2.id}

        response = self.client.post(url, headers=headers)

        expected_response = {
            'message': 'Successfully unsubscribed'
        }

        # Assert the response status code
        self.assertEqual(response.status_code, 200)

        # Assert the response data
        self.assertEqual(response.data, expected_response)

    def test_unsubscribe_not_subscribed(self):
        url = reverse('unsubscribe', args=[self.user1.id])
        headers = {'User-id': self.user2.id}

        response = self.client.post(url, headers=headers)

        expected_response = {
            'error': 'Not currently subscribed to this user'
        }

        # Assert the response status code
        self.assertEqual(response.status_code, 400)

        # Assert the response data
        self.assertEqual(response.data, expected_response)

    def test_get_subscriptions(self):
        url = reverse('get_subscriptions')
        headers = {'User-id': self.user1.id}

        response = self.client.get(url, headers=headers) 

        # Assert the response status code
        self.assertEqual(response.status_code, 200)
    
    '''
    @patch('noteally_app.webservices.ws_user.boto3')
    def test_user_sns_topic_creation(self, mock_boto3):
        # mock response from boto3
        mock_boto3.client.return_value = MagicMock()
        mock_boto3.client.return_value.create_topic.return_value = {'TopicArn': 'test_topic_arn'}

        # Subscribe the user to the SNS topic to allow notifications of new uploads
        topic_name = f'uploads-user-{self.user_to_follow.id}'
        topic_arn = f'arn:aws:sns:{settings.AWS_REGION_NAME}:{settings.AWS_ACCOUNT_ID}:{topic_name}'

        response = subscribe_to_sns_topic(self.user, self.user_to_follow)

        # Assert the response status code
        self.assertEqual(response.status_code, 200)

        # Assert the topic creation
        mock_boto3.client.create_topic.assert_called_once_with(Name=topic_name)
    '''
        
 
        
        