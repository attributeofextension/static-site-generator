import unittest

from main import text_node_to_html_node
from textnode import TextNode
from htmlnode import LeafNode


class TestTextNodeToHTML(unittest.TestCase):
    def setUp(self):
        self.text_type_text_node = TextNode("raw text", "text","not shown", "raw text")
        self.text_type_bold_node = TextNode("bold text", "bold", "not shown", "**bold text**")
        self.text_type_italic_node = TextNode("italic text", "italic", "not shown", "*italic text*")
        self.text_type_code_node = TextNode("code text", "code", "not shown", "`code text`")
        self.text_type_link_node = TextNode("link text", "link", "shown in href prop", "link text")
        self.text_type_image_node = TextNode("shown in alt prop", "image", "shown in src prop", "image text")
        self.text_type_script_node = TextNode("raises exception", "script", "not shown", "raises exception")

    def test_text_type_text(self):
        node = text_node_to_html_node(self.text_type_text_node)
        self.assertIsInstance(node, LeafNode)
        self.assertEqual(node.to_html(), "raw text")
        self.assertEqual(node.to_html(), self.text_type_text_node.text)

    def test_text_type_bold(self):
        node = text_node_to_html_node(self.text_type_bold_node)
        self.assertIsInstance(node, LeafNode)
        self.assertEqual(node.to_html(), "<b>bold text</b>")
        self.assertIn(self.text_type_bold_node.text, node.to_html())
        self.assertEqual(node.to_html()[0:3], "<b>")
        self.assertEqual(node.to_html()[-4:], "</b>")

    def test_text_type_italic(self):
        node = text_node_to_html_node(self.text_type_italic_node)
        self.assertIsInstance(node, LeafNode)
        self.assertEqual(node.to_html(), "<i>italic text</i>")
        self.assertIn(self.text_type_italic_node.text, node.to_html())
        self.assertEqual(node.to_html()[0:3], "<i>")
        self.assertEqual(node.to_html()[-4:], "</i>")

    def test_text_type_code(self):
        node = text_node_to_html_node(self.text_type_code_node)
        self.assertIsInstance(node, LeafNode)
        self.assertEqual(node.to_html(), "<code>code text</code>")
        self.assertIn(self.text_type_code_node.text, node.to_html())
        self.assertEqual(node.to_html()[0:6], "<code>")
        self.assertEqual(node.to_html()[-7:], "</code>")

    def test_text_type_link(self):
        node = text_node_to_html_node(self.text_type_link_node)
        self.assertIsInstance(node, LeafNode)
        self.assertEqual(node.to_html(), "<a href=\"shown in href prop\">link text</a>")
        self.assertIn(self.text_type_link_node.text, node.to_html())
        self.assertIn("href", node.to_html())
        self.assertIn(self.text_type_link_node.url, node.to_html())
        self.assertEqual(node.to_html()[0:2],"<a")
        self.assertEqual(node.to_html()[-4:], "</a>")

    def test_text_type_image(self):
        node = text_node_to_html_node(self.text_type_image_node)
        self.assertIsInstance(node, LeafNode)
        self.assertEqual(node.to_html(), "<img src=\"shown in src prop\" alt=\"shown in alt prop\"></img>")
        self.assertIn(self.text_type_image_node.text, node.to_html())
        self.assertIn("src", node.to_html())
        self.assertIn(self.text_type_image_node.url, node.to_html())
        self.assertIn("alt", node.to_html())
        self.assertEqual(node.to_html()[0:4],"<img")
        self.assertEqual(node.to_html()[-6:], "</img>")

    def test_text_type_script(self):
        with self.assertRaisesRegex(Exception, "Text node type is not acceptable"):
            node = text_node_to_html_node(self.text_type_script_node)


if __name__ == '__main__':
    unittest.main()
