import unittest

from textnode import TextNode


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", "bold","test")
        node2 = TextNode("This is a text node", "bold", "test")
        self.assertEqual(node, node2)

    def test_eq_2(self):
        node = TextNode("Test", "test", None)
        node2 = TextNode("Test","test", None)
        self.assertEqual(node,node2)

    def test_not_eq(self):
        node = TextNode("Test1", "test", "test")
        node2 = TextNode("Test2", "test", "test")
        self.assertNotEqual(node, node2)

if __name__ == "__main__":
    unittest.main()