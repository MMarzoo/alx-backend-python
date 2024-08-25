#!/usr/bin/env python3
""" Module for testing utils """

import unittest
from unittest.mock import patch, Mock
from parameterized import parameterized
from utils import (access_nested_map, get_json, memoize)


class TestAccessNestedMap(unittest.TestCase):
    """ Class for Testing Access Nested Map """

    @parameterized.expand([
        ({"a": 1}, ("a",), 1),
        ({"a": {"b": 2}}, ("a",), {'b': 2}),
        ({"a": {"b": 2}}, ("a", "b"), 2)
    ])
    def test_access_nested_map(self, nested_map, path, expected):
        """ Test that the method returns what it is supposed to """
        self.assertEqual(access_nested_map(nested_map, path), expected)

    @parameterized.expand(
        [({}, ("a",), KeyError), ({"a": 1}, ("a", "b"), KeyError)]
    )
    def test_access_nested_map_exception(self, nested_map,
                                         path, expected_exception):
        """ Test that the method raises the expected exception """
        with self.assertRaises(expected_exception):
            access_nested_map(nested_map, path)


class TestGetJson(unittest.TestCase):
    """ Class for Testing Get Json """
    @parameterized.expand([
        ("http://example.com", {"payload": True}),
        ("http://holberton.io", {"payload": False}),
    ])
    def test_get_json(self, url, payload):
        """ Test that the method returns the expected payload """
        mock = Mock()
        mock.json.return_value = payload
        with patch("requests.get", return_value=mock):
            self.assertEqual(get_json(url), payload)


class TestMemoize(unittest.TestCase):
    """ Class for Testing Memoize """
    def test_memoize(self):
        """ Test that the method returns the expected result """

        class TestClass:
            """ Test Class for wrapping with memoize """

            def a_method(self):
                """ Method to be memoized """
                return 42

            @memoize
            def a_property(self):
                """ Property to be memoized """
                return self.a_method()

        with patch.object(TestClass, 'a_method') as mock:
            test_class = TestClass()
            test_class.a_property()
            test_class.a_property()
            mock.assert_called_once()
