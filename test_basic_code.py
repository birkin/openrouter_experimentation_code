"""
Unit tests for basic_code.py.
"""

import json
import unittest
from unittest.mock import MagicMock, mock_open, patch

import httpx

import basic_code


class TestBasicCode(unittest.TestCase):
    """
    Checks that basic_code behavior matches expectations.
    """

    @patch('basic_code.load_dotenv')
    @patch.dict(
        'basic_code.os.environ',
        {
            'OPENROUTER_API_KEY': 'test-api-key',
            'OPENROUTER_MODEL': 'test-model',
            'OPENROUTER_PROMPT_FILE': '/tmp/test_prompt.txt',
        },
        clear=True,
    )
    def test_load_config_reads_required_env_vars(self, mock_load_dotenv: MagicMock):
        """
        Checks that load_config reads required environment variables.
        """
        api_key, model, prompt_file = basic_code.load_config()
        self.assertEqual(api_key, 'test-api-key')
        self.assertEqual(model, 'test-model')
        self.assertEqual(prompt_file, '/tmp/test_prompt.txt')
        mock_load_dotenv.assert_called_once()

    @patch('builtins.open', new_callable=mock_open, read_data='hello prompt')
    def test_load_prompt_reads_file_contents(self, mock_file: MagicMock):
        """
        Checks that load_prompt reads the full prompt contents.
        """
        prompt = basic_code.load_prompt('/tmp/prompt.txt')
        self.assertEqual(prompt, 'hello prompt')
        mock_file.assert_called_once_with('/tmp/prompt.txt', 'r')

    @patch('basic_code.httpx.post')
    def test_call_openrouter_builds_expected_http_request(self, mock_post: MagicMock):
        """
        Checks that call_openrouter calls httpx.post with expected URL, headers, and JSON payload.
        """
        mock_response = MagicMock(spec=httpx.Response)
        mock_response.json.return_value = {'choices': [{'message': {'content': 'ok'}}]}
        mock_post.return_value = mock_response

        result = basic_code.call_openrouter('k', 'm', 'p')
        self.assertEqual(result, {'choices': [{'message': {'content': 'ok'}}]})

        mock_post.assert_called_once()
        kwargs = mock_post.call_args.kwargs

        self.assertEqual(kwargs['url'], 'https://openrouter.ai/api/v1/chat/completions')
        self.assertEqual(kwargs['headers'], {'Authorization': 'Bearer k'})

        payload = json.loads(kwargs['data'])
        self.assertEqual(
            payload,
            {
                'model': 'm',
                'transforms': ['middle-out'],
                'messages': [{'role': 'user', 'content': 'p'}],
            },
        )

    @patch('builtins.print')
    @patch('basic_code.call_openrouter')
    @patch('basic_code.load_prompt')
    @patch('basic_code.load_config')
    def test_main_orchestrates_calls_and_prints(
        self, mock_load_config: MagicMock, mock_load_prompt: MagicMock, mock_call: MagicMock, mock_print: MagicMock
    ):
        """
        Checks that main loads config and prompt, calls OpenRouter, and prints output.
        """
        mock_load_config.return_value = ('k', 'm', '/tmp/prompt.txt')
        mock_load_prompt.return_value = 'p'
        mock_call.return_value = {'ok': True}

        basic_code.main()

        mock_load_config.assert_called_once()
        mock_load_prompt.assert_called_once_with('/tmp/prompt.txt')
        mock_call.assert_called_once_with('k', 'm', 'p')

        expected_json = json.dumps({'ok': True}, indent=2)
        mock_print.assert_any_call(expected_json)

        time_print_calls = [
            call
            for call in mock_print.call_args_list
            if call.args and isinstance(call.args[0], str) and call.args[0].startswith('time taken,')
        ]
        self.assertGreaterEqual(len(time_print_calls), 1)


if __name__ == '__main__':
    unittest.main()
