import unittest

from functions import *
from classes import Node


class TestFunctions(unittest.TestCase):
    def test_text(self):
        ans1 = Node(markdown_to_blocks("test")[0]).get_HTML()
        ans2 = "<p>test</p>"

        self.assertEqual(ans1, ans2)

if __name__ == "__main__":
    unittest.main()