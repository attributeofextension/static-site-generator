import unittest

from textnode import TextNode
from htmlnode import HTMLNode, LeafNode


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

class TestHTMLNode(unittest.TestCase):
    def test_props_to_html(self):
        node1 = HTMLNode(None, None, None, {"href": "https://www.google.com", "target": "_blank"})
        self.assertEqual(node1.props_to_html()," href=\"https://www.google.com\" target=\"_blank\"")

    def test_to_html(self):
        node1 = HTMLNode(None, None, None, {"href": "https://www.google.com", "target": "_blank"})
        with self.assertRaises(NotImplementedError):
            node1.to_html()

class TestLeafNode(unittest.TestCase):
    def test_to_html(self):
        node1 = LeafNode("This is a paragraph of text.", "p")
        self.assertEqual(node1.to_html(), "<p>This is a paragraph of text.</p>")

    def test_to_html_no_tag(self):
        node1 = LeafNode("This is a paragraph of text.")
        self.assertEqual(node1.to_html(),"This is a paragraph of text.")

    def test_to_html_no_value(self):
        node1 = LeafNode(None)
        with self.assertRaises(ValueError):
            node1.to_html()

if __name__ == "__main__":
    unittest.main()