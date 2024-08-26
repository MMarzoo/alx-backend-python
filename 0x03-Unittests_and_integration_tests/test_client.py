#!/usr/bin/env python3
"""
Unittest Test client
"""

import unittest
from unittest.mock import Mock, patch, PropertyMock
from parameterized import parameterized, parameterized_class
from client import GithubOrgClient
from fixtures import TEST_PAYLOAD


class TestGithubOrgClient(unittest.TestCase):
    """ TestGithubOrgClient class """

    @parameterized.expand([
        ('google'),
        ('abc')
    ])
    @patch('client.get_json')
    def test_org(self, data, mock):
        ''' self descriptive '''
        endpoint = 'https://api.github.com/orgs/{}'.format(data)
        spec = GithubOrgClient(data)
        spec.org()
        mock.assert_called_once_with(endpoint)

    def test_public_repos_url(self):
        """ Test that _public_repos_url method returns the expected result """
        with patch(
            'client.GithubOrgClient.org', new_callable=PropertyMock
        ) as mock_org:
            spec = GithubOrgClient("google")
            self.assertEqual(
                spec._public_repos_url,
                mock_org.return_value["repos_url"]
            )

    @patch('client.get_json')
    def test_public_repos(self, mock_get_json):
        """ Test that public_repos method returns the expected result """
        TEST_PAYLOAD = [{"name": "Google"}, {"name": "TT"}]
        mock_get_json.return_value = TEST_PAYLOAD
        url = "https://api.github.com/orgs/google/repos"
        with patch(
            'client.GithubOrgClient._public_repos_url',
            new_callable=PropertyMock,
            return_value=url
        ) as mock_repos_url:
            spec = GithubOrgClient("google")
            result = spec.public_repos()
            self.assertEqual(result, ["Google", "TT"])
            mock_get_json.assert_called_once_with(url)
            mock_repos_url.assert_called_once()

    @parameterized.expand([
        ({"license": {"key": "my_license"}}, "my_license", True),
        ({"license": {"key": "other_license"}}, "my_license", False)
    ])
    def test_has_license(self, repo, key, expectation):
        """ Test that license method returns the expected result """
        result = GithubOrgClient.has_license(repo, key)
        self.assertEqual(result, expectation)


@parameterized_class(['org_payload', 'repos_payload',
                      'expected_repos', 'apache2_repos'], TEST_PAYLOAD)
class TestIntegrationGithubOrgClient(unittest.TestCase):
    """Integration test"""
    @classmethod
    def setUpClass(cls):
        cls.get_patcher = patch('requests.get', side_effect=[
            cls.org_payload, cls.repos_payload
        ])
        cls.mocked_get = cls.get_patcher.start()

    @classmethod
    def tearDownClass(cls):
        cls.get_patcher.stop()
