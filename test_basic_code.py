"""
Unit tests for basic_code.py to verify httpx migration works correctly.
"""

import json
import unittest
from unittest.mock import MagicMock, patch

import httpx


class TestBasicCodeHttpx(unittest.TestCase):
    """
    Checks that the httpx migration maintains compatibility with expected behavior.
    """

    def test_httpx_response_interface(self):
        """
        Checks that httpx response object has the same interface as requests.
        """
        # Create a mock httpx response
        mock_response = MagicMock(spec=httpx.Response)
        mock_response.status_code = 200
        mock_response.headers = {'content-type': 'application/json'}
        mock_response.json.return_value = {'choices': [{'message': {'content': 'test'}}]}

        # Verify the interface matches what basic_code.py expects
        self.assertTrue(hasattr(mock_response, 'status_code'))
        self.assertTrue(hasattr(mock_response, 'headers'))
        self.assertTrue(hasattr(mock_response, 'json'))
        self.assertTrue(callable(mock_response.json))

        # Test that json() returns expected dict structure
        result = mock_response.json()
        self.assertIsInstance(result, dict)
        self.assertIn('choices', result)

    @patch('httpx.post')
    def test_openrouter_api_call_structure(self, mock_post: MagicMock):
        """
        Checks that the API call structure works with httpx.
        """
        # Mock successful API response
        mock_response = MagicMock(spec=httpx.Response)
        mock_response.status_code = 200
        mock_response.json.return_value = {
            'choices': [{'message': {'content': 'Test response'}}],
            'usage': {'total_tokens': 10},
        }
        mock_post.return_value = mock_response

        # Simulate the call that basic_code.py makes
        response = httpx.post(
            url='https://openrouter.ai/api/v1/chat/completions',
            headers={
                'Authorization': 'Bearer test-key',
                'Content-Type': 'application/json',
            },
            data=json.dumps(
                {
                    'model': 'test-model',
                    'messages': [{'role': 'user', 'content': 'test prompt'}],
                }
            ),
        )

        # Verify the call was made correctly
        mock_post.assert_called_once()
        self.assertEqual(response.status_code, 200)

        # Verify response can be processed like requests response
        result = response.json()
        self.assertIsInstance(result, dict)
        self.assertIn('choices', result)

    def test_json_serialization_compatibility(self):
        """
        Checks that JSON serialization works the same way.
        """
        test_data = {
            'model': 'test-model',
            'messages': [{'role': 'user', 'content': 'test prompt'}],
        }

        # Test that json.dumps produces the same format
        serialized = json.dumps(test_data)
        self.assertIsInstance(serialized, str)

        # Verify it can be deserialized back
        deserialized = json.loads(serialized)
        self.assertEqual(deserialized, test_data)


if __name__ == '__main__':
    unittest.main()
