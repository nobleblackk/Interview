import unittest
from um_cli import fuzzy_match_command
from commands import create_user, delete_user, update_user, list_users

class FuzzyMatchCommandTestCase(unittest.TestCase):

    def test_exact_match(self):
        command = "create"
        matches = fuzzy_match_command(command)
        self.assertIn(matches, ["create"])

    def test_partial_match(self):
        command = "crte"
        matches = fuzzy_match_command(command)
        self.assertIn(matches, ['create'])

    def test_no_match(self):
        command = "abcde"
        matches = fuzzy_match_command(command)
        self.assertIn(matches, [None])

    def test_threshold_match(self):
        command = "crat"
        matches = fuzzy_match_command(command, threshold=0.6)
        self.assertIn(matches, ["create"])


if __name__ == '__main__':
    unittest.main()
