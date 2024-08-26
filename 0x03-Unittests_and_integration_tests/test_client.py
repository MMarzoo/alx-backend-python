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
        """Set up the test environment by mocking requests.get"""
        cls.get_patcher = patch('requests.get')
        cls.mock_get = cls.get_patcher.start()

        def get_json_side_effect(url: str):
            """Return different mock responses based on the URL"""
            mock = Mock()
            if url == cls.org_payload["repos_url"]:
                mock.json.return_value = cls.repos_payload
            else:
                mock.json.return_value = cls.org_payload
            return mock

        cls.mock_get.side_effect = get_json_side_effect

    @classmethod
    def tearDownClass(cls):
        """ Clean up the test environment """
        cls.get_patcher.stop()

    def test_public_repos(self):
        """ Test that public_repos method returns the expected result """
        test_class = GithubOrgClient("google")
        self.assertEqual(test_class.org, self.org_payload)
        self.assertEqual(test_class.repos_payload, self.repos_payload)
        self.assertEqual(test_class.public_repos(), self.expected_repos)
        self.assertEqual(test_class.public_repos("404"), [])

    def test_public_repos_with_license(self):
        """ Test that public_repos method returns the expected result """
        spec = GithubOrgClient("google")
        self.assertEqual(spec.public_repos("apache-2.0"), self.apache2_repos)
