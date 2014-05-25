import sys
import unittest

sys.path.append("../")
from kill_django.kill_django import find_pids


class TestKillDjango(unittest.TestCase):
    def test_find_pids(self):
        processes = [
            'user     1111 foo bar',
            'user      1112 foo bar baz',
        ]
        actual = []
        generator = find_pids(processes)
        for pid in generator:
            actual.append(pid)
        self.assertEqual(actual, ['1111', '1112'])
