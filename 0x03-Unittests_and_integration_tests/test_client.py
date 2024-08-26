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
            'client.GithubOrgClient.org', new_callable= PropertyMock
        ) as mock_org:
            spec = GithubOrgClient("google")
            self.assertEqual(
                spec._public_repos_url,
                mock_org.return_value["repos_url"]
            )
