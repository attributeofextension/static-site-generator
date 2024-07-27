import unittest

from textnode import TextNode
from htmlnode import HTMLNode, ParentNode, LeafNode
import re


class TestTextNode(unittest.TestCase):


    def test_eq(self):
        node = TextNode("This is a text node", "bold","test", "This is a text node")
        node2 = TextNode("This is a text node", "bold", "test", "This is a text node")
        self.assertEqual(node, node2)

    def test_eq_2(self):
        node = TextNode("Test", "test", None, "Test")
        node2 = TextNode("Test","test", None, "Test")
        self.assertEqual(node,node2)

    def test_not_eq(self):
        node = TextNode("Test1", "test", "test", "Test")
        node2 = TextNode("Test2", "test", "test", "Test")
        self.assertNotEqual(node, node2)

    def test_image_text_type(self):
        text_node = TextNode("alt text", "image", "/url")
        html_node = text_node.to_html_node()
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.props["alt"], "alt text")
        self.assertEqual(html_node.props["src"], "/url")
        self.assertIsNone(html_node.children)

    def test_image_text_type_with_children(self):
        text_node = TextNode("alt text", "image", "/url", )
        text_node.children.append(TextNode("text node", "text",))
        html_node = text_node.to_html_node()
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.props["alt"], "alt text")
        self.assertEqual(html_node.props["src"], "/url")
        self.assertIsNone(html_node.children)

    def test_text_type_link(self):
        text_node = TextNode("link text", "link", "/url")
        html_node = text_node.to_html_node()
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.props["href"], "/url")
        self.assertEqual(html_node.value, "link text")
        self.assertIsNone(html_node.children)

    def test_text_type_link_with_children(self):
        text_node = TextNode("link text", "link", "/url", )
        text_node.children.append(TextNode("text node", "text"))
        html_node = text_node.to_html_node()
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.props["href"], "/url")
        self.assertEqual(html_node.value, "link text")
        self.assertIsNone(html_node.children)

    def test_text_type_h1(self):
        text_node = TextNode("Heading 1", "h1")
        html_node = text_node.to_html_node()
        self.assertEqual(html_node.tag, "h1")
        self.assertEqual(html_node.value, "Heading 1")
        self.assertIsNone(html_node.props)
        self.assertIsNone(html_node.children)

    def test_text_type_h1_with_children(self):
        text_node = TextNode("Heading 1", "h1")
        text_node.children.append(TextNode("Text node text 1 ", "text"))
        text_node.children.append(TextNode("bold text", "bold"))
        text_node.children.append(TextNode(" the last bit", "text"))
        html_node = text_node.to_html_node()
        self.assertEqual(html_node.tag, "h1")
        self.assertNotEqual(html_node.value, "Heading 1")
        self.assertIsNone(html_node.value)
        self.assertIsNone(html_node.props)
        self.assertIsNotNone(html_node.children)
        self.assertEqual(len(html_node.children), 3)

        self.assertEqual(html_node.children[0].tag, "")
        self.assertEqual(html_node.children[1].tag, "b")
        self.assertEqual(html_node.children[2].tag, "")

    def test_text_type_h2(self):
        text_node = TextNode("Heading 2", "h2")
        html_node = text_node.to_html_node()
        self.assertEqual(html_node.tag, "h2")
        self.assertEqual(html_node.value, "Heading 2")
        self.assertIsNone(html_node.props)
        self.assertIsNone(html_node.children)

    def test_text_type_h2_with_children(self):
        text_node = TextNode("Heading 2", "h2")
        text_node.children.append(TextNode("Text node text 1 ", "text"))
        text_node.children.append(TextNode("bold text", "bold"))
        text_node.children.append(TextNode(" the last bit", "text"))
        html_node = text_node.to_html_node()
        self.assertEqual(html_node.tag, "h2")
        self.assertNotEqual(html_node.value, "Heading 2")
        self.assertIsNone(html_node.value)
        self.assertIsNone(html_node.props)
        self.assertIsNotNone(html_node.children)
        self.assertEqual(len(html_node.children), 3)

        self.assertEqual(html_node.children[0].tag, "")
        self.assertEqual(html_node.children[1].tag, "b")
        self.assertEqual(html_node.children[2].tag, "")

    def test_text_type_h3(self):
        text_node = TextNode("Heading 3", "h3")
        html_node = text_node.to_html_node()
        self.assertEqual(html_node.tag, "h3")
        self.assertEqual(html_node.value, "Heading 3")
        self.assertIsNone(html_node.props)
        self.assertIsNone(html_node.children)

    def test_text_type_h3_with_children(self):
        text_node = TextNode("Heading 3", "h3")
        text_node.children.append(TextNode("Text node text 1 ", "text"))
        text_node.children.append(TextNode("bold text", "bold"))
        text_node.children.append(TextNode(" the last bit", "text"))
        html_node = text_node.to_html_node()
        self.assertEqual(html_node.tag, "h3")
        self.assertNotEqual(html_node.value, "Heading 3")
        self.assertIsNone(html_node.value)
        self.assertIsNone(html_node.props)
        self.assertIsNotNone(html_node.children)
        self.assertEqual(len(html_node.children), 3)

        self.assertEqual(html_node.children[0].tag, "")
        self.assertEqual(html_node.children[1].tag, "b")
        self.assertEqual(html_node.children[2].tag, "")

    def test_text_type_h4(self):
        text_node = TextNode("Heading 4", "h4")
        html_node = text_node.to_html_node()
        self.assertEqual(html_node.tag, "h4")
        self.assertEqual(html_node.value, "Heading 4")
        self.assertIsNone(html_node.props)
        self.assertIsNone(html_node.children)

    def test_text_type_h4_with_children(self):
        text_node = TextNode("Heading 4", "h4")
        text_node.children.append(TextNode("Text node text 1 ", "text"))
        text_node.children.append(TextNode("bold text", "bold"))
        text_node.children.append(TextNode(" the last bit", "text"))
        html_node = text_node.to_html_node()
        self.assertEqual(html_node.tag, "h4")
        self.assertNotEqual(html_node.value, "Heading 4")
        self.assertIsNone(html_node.value)
        self.assertIsNone(html_node.props)
        self.assertIsNotNone(html_node.children)
        self.assertEqual(len(html_node.children), 3)

        self.assertEqual(html_node.children[0].tag, "")
        self.assertEqual(html_node.children[1].tag, "b")
        self.assertEqual(html_node.children[2].tag, "")

    def test_text_type_h5(self):
        text_node = TextNode("Heading 5", "h5")
        html_node = text_node.to_html_node()
        self.assertEqual(html_node.tag, "h5")
        self.assertEqual(html_node.value, "Heading 5")
        self.assertIsNone(html_node.props)
        self.assertIsNone(html_node.children)

    def test_text_type_h5_with_children(self):
        text_node = TextNode("Heading 5", "h5")
        text_node.children.append(TextNode("Text node text 1 ", "text"))
        text_node.children.append(TextNode("bold text", "bold"))
        text_node.children.append(TextNode(" the last bit", "text"))
        html_node = text_node.to_html_node()
        self.assertEqual(html_node.tag, "h5")
        self.assertNotEqual(html_node.value, "Heading 5")
        self.assertIsNone(html_node.value)
        self.assertIsNone(html_node.props)
        self.assertIsNotNone(html_node.children)
        self.assertEqual(len(html_node.children), 3)

        self.assertEqual(html_node.children[0].tag, "")
        self.assertEqual(html_node.children[1].tag, "b")
        self.assertEqual(html_node.children[2].tag, "")

    def test_text_type_paragraph(self):
        text_node = TextNode("Paragraph", "paragraph")
        html_node = text_node.to_html_node()
        self.assertEqual(html_node.tag, "p")
        self.assertEqual(html_node.value, "Paragraph")
        self.assertIsNone(html_node.props)
        self.assertIsNone(html_node.children)

    def test_text_type_paragraph_with_children(self):
        text_node = TextNode("Paragraph", "paragraph")
        text_node.children.append(TextNode("Text node text 1 ", "text"))
        text_node.children.append(TextNode("bold text", "bold"))
        text_node.children.append(TextNode(" the last bit", "text"))
        html_node = text_node.to_html_node()
        self.assertEqual(html_node.tag, "p")
        self.assertNotEqual(html_node.value, "Paragraph")
        self.assertIsNone(html_node.value)
        self.assertIsNone(html_node.props)
        self.assertIsNotNone(html_node.children)
        self.assertEqual(len(html_node.children), 3)

        self.assertEqual(html_node.children[0].tag, "")
        self.assertEqual(html_node.children[1].tag, "b")
        self.assertEqual(html_node.children[2].tag, "")

    def test_text_type_bold(self):
        text_node = TextNode("Bold", "bold")
        html_node = text_node.to_html_node()
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "Bold")
        self.assertIsNone(html_node.props)
        self.assertIsNone(html_node.children)

    def test_text_type_bold_with_children(self):
        text_node = TextNode("Bold", "bold")
        text_node.children.append(TextNode("Text node text 1 ", "text"))
        text_node.children.append(TextNode("italic text", "italic"))
        text_node.children.append(TextNode(" the last bit", "text"))
        html_node = text_node.to_html_node()
        self.assertEqual(html_node.tag, "b")
        self.assertNotEqual(html_node.value, "Bold")
        self.assertIsNone(html_node.value)
        self.assertIsNone(html_node.props)
        self.assertIsNotNone(html_node.children)
        self.assertEqual(len(html_node.children), 3)
        self.assertEqual(html_node.children[0].tag, "")
        self.assertEqual(html_node.children[1].tag, "i")
        self.assertEqual(html_node.children[2].tag, "")

    def test_text_type_italic(self):
        text_node = TextNode("Italic", "italic")
        html_node = text_node.to_html_node()
        self.assertEqual(html_node.tag, "i")
        self.assertEqual(html_node.value, "Italic")
        self.assertIsNone(html_node.props)
        self.assertIsNone(html_node.children)

    def test_text_type_italic_with_children(self):
        text_node = TextNode("Italic", "italic")
        text_node.children.append(TextNode("Text node text 1 ", "text"))
        text_node.children.append(TextNode("bold text", "bold"))
        text_node.children.append(TextNode(" the last bit", "text"))
        html_node = text_node.to_html_node()
        self.assertEqual(html_node.tag, "i")
        self.assertNotEqual(html_node.value, "Italic")
        self.assertIsNone(html_node.value)
        self.assertIsNone(html_node.props)
        self.assertIsNotNone(html_node.children)
        self.assertEqual(len(html_node.children), 3)
        self.assertEqual(html_node.children[0].tag, "")
        self.assertEqual(html_node.children[1].tag, "b")
        self.assertEqual(html_node.children[2].tag, "")

    def test_text_type_ul_item(self):
        text_node = TextNode("Unordered List Item", "ul-item")
        html_node = text_node.to_html_node()
        self.assertEqual(html_node.tag, "li")
        self.assertEqual(html_node.value, "Unordered List Item")
        self.assertIsNone(html_node.props)
        self.assertIsNone(html_node.children)

    def test_text_type_ul_item_with_children(self):
        text_node = TextNode("Unordered List Item", "ul-item")
        text_node.children.append(TextNode("Text node text 1 ", "text"))
        text_node.children.append(TextNode("bold text", "bold"))
        text_node.children.append(TextNode(" the last bit", "text"))
        html_node = text_node.to_html_node()
        self.assertEqual(html_node.tag, "li")
        self.assertNotEqual(html_node.value, "Unordered List Item")
        self.assertIsNone(html_node.value)
        self.assertIsNone(html_node.props)
        self.assertIsNotNone(html_node.children)
        self.assertEqual(len(html_node.children), 3)
        self.assertEqual(html_node.children[0].tag, "")
        self.assertEqual(html_node.children[1].tag, "b")
        self.assertEqual(html_node.children[2].tag, "")

    def test_text_type_ol_item(self):
        text_node = TextNode("Ordered List Item", "ol-item")
        html_node = text_node.to_html_node()
        self.assertEqual(html_node.tag, "li")
        self.assertEqual(html_node.value, "Ordered List Item")
        self.assertIsNone(html_node.props)
        self.assertIsNone(html_node.children)

    def test_text_type_ol_item_with_children(self):
        text_node = TextNode("Ordered List Item", "ol-item")
        text_node.children.append(TextNode("Text node text 1 ", "text"))
        text_node.children.append(TextNode("bold text", "bold"))
        text_node.children.append(TextNode(" the last bit", "text"))
        html_node = text_node.to_html_node()
        self.assertEqual(html_node.tag, "li")
        self.assertNotEqual(html_node.value, "Ordered List Item")
        self.assertIsNone(html_node.value)
        self.assertIsNone(html_node.props)
        self.assertIsNotNone(html_node.children)
        self.assertEqual(len(html_node.children), 3)
        self.assertEqual(html_node.children[0].tag, "")
        self.assertEqual(html_node.children[1].tag, "b")
        self.assertEqual(html_node.children[2].tag, "")

    def test_text_type_ol_with_ol_item_children_only(self):
        text_node = TextNode("Ordered List", "ol")
        text_node.children.append(TextNode("Ordered List Item 1", "ol-item"))
        text_node.children.append(TextNode("Ordered List Item 2", "ol-item"))
        text_node.children.append(TextNode("Ordered List Item 3", "ol-item"))
        html_node = text_node.to_html_node()
        self.assertEqual(html_node.tag, "ol")
        self.assertNotEqual(html_node.value, "Ordered List")
        self.assertIsNone(html_node.value)
        self.assertIsNone(html_node.props)
        self.assertIsNotNone(html_node.children)
        self.assertEqual(len(html_node.children), 3)
        self.assertEqual(html_node.children[0].tag, "li")
        self.assertEqual(html_node.children[1].tag, "li")
        self.assertEqual(html_node.children[2].tag, "li")

    def test_text_type_ol_with_other_children(self):
        text_node = TextNode("Ordered List", "ol")
        text_node.children.append(TextNode("Text", "text"))
        with self.assertRaises(Exception):
            text_node.to_html_node()

    def test_text_type_ol_with_no_children(self):
        text_node = TextNode("Ordered List", "ol")
        with self.assertRaises(Exception):
            html_node = text_node.to_html_node()

    def test_text_type_ul_with_ul_item_children_only(self):
        text_node = TextNode("Unordered List", "ul")
        text_node.children.append(TextNode("Unordered List Item 1", "ul-item"))
        text_node.children.append(TextNode("Unordered List Item 2", "ul-item"))
        text_node.children.append(TextNode("Unordered List Item 3", "ul-item"))
        html_node = text_node.to_html_node()
        self.assertEqual(html_node.tag, "ul")
        self.assertNotEqual(html_node.value, "Unordered List")
        self.assertIsNone(html_node.value)
        self.assertIsNone(html_node.props)
        self.assertIsNotNone(html_node.children)
        self.assertEqual(len(html_node.children), 3)
        self.assertEqual(html_node.children[0].tag, "li")
        self.assertEqual(html_node.children[1].tag, "li")
        self.assertEqual(html_node.children[2].tag, "li")

    def test_text_type_ul_with_other_children(self):
        text_node = TextNode("Unordered List", "ul")
        text_node.children.append(TextNode("Text", "text"))
        with self.assertRaises(Exception):
            html_node = text_node.to_html_node()

    def test_text_type_ul_with_no_children(self):
        text_node = TextNode("Unordered List", "ul")
        with self.assertRaises(Exception):
            html_node = text_node.to_html_node()

    def test_text_type_quote_with_no_children(self):
        text_node = TextNode("A quote", "quote")
        html_node = text_node.to_html_node()
        self.assertEqual(html_node.tag, "blockquote")
        self.assertEqual(html_node.value, "A quote")
        self.assertIsNone(html_node.children)

    def test_text_type_quote_with_children(self):
        text_node = TextNode("A quote", "quote")
        text_node.children.append(TextNode("Text node text 1 ", "text"))
        text_node.children.append(TextNode("Text node text 2 ", "text"))
        text_node.children.append(TextNode("Text node text 3 ", "text"))
        html_node = text_node.to_html_node()
        self.assertEqual(html_node.tag, "blockquote")
        self.assertEqual(html_node.value, "A quote")
        self.assertIsNone(html_node.children)

    def test_text_type_code_block_with_no_children(self):
        text_node = TextNode("A code block", "code-block")
        html_node = text_node.to_html_node()
        self.assertEqual(html_node.tag, "pre")
        self.assertEqual(html_node.value, None)
        self.assertIsNotNone(html_node.children)
        self.assertEqual(len(html_node.children), 1)
        self.assertEqual(html_node.children[0].tag, "code")
        self.assertEqual(html_node.children[0].value, "A code block")

    def test_text_type_code_block_with_children(self):
        text_node = TextNode("A code block", "code-block")
        text_node.children.append(TextNode("Text node text 1 ", "text"))
        text_node.children.append(TextNode("Text node text 2 ", "text"))
        text_node.children.append(TextNode("Text node text 3 ", "text"))
        html_node = text_node.to_html_node()
        self.assertEqual(html_node.tag, "pre")
        self.assertEqual(html_node.value, None)
        self.assertIsNotNone(html_node.children)
        self.assertEqual(len(html_node.children), 1)
        self.assertEqual(html_node.children[0].tag, "code")
        self.assertEqual(html_node.children[0].value, "A code block")
        self.assertIsNone(html_node.children[0].children)

    def test_text_type_code_with_no_children(self):
        text_node = TextNode("some code", "code")
        html_node = text_node.to_html_node()
        self.assertEqual(html_node.tag, "code")
        self.assertEqual(html_node.value, "some code")
        self.assertIsNone(html_node.children)

    def test_text_type_code_with_children(self):
        text_node = TextNode("some code", "code")
        text_node.children.append(TextNode("Text node text 1 ", "text"))
        text_node.children.append(TextNode("Text node text 2 ", "text"))
        text_node.children.append(TextNode("Text node text 3 ", "text"))
        html_node = text_node.to_html_node()
        self.assertEqual(html_node.tag, "code")
        self.assertEqual(html_node.value, "some code")
        self.assertIsNone(html_node.children)


if __name__ == "__main__":
    unittest.main()