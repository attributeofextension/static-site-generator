import unittest

from htmlnode import HTMLNode, ParentNode, LeafNode

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
        with self.assertRaisesRegex(ValueError, "Value cannot be None"):
            node1.to_html()

class TestParentNode(unittest.TestCase):
    def test_to_html_children_is_none(self):
        node1 = ParentNode(None, "ul")
        with self.assertRaisesRegex(ValueError, "Children cannot be None"):
            node1.to_html()

    def test_to_html_children_is_empty(self):
        node1 = ParentNode([], "ul")
        with self.assertRaisesRegex(ValueError, "Children cannot be empty"):
            node1.to_html()

    def test_to_html_tag_is_none(self):
        node1 = ParentNode([LeafNode("This is a paragraph of text.")], None)
        with self.assertRaisesRegex(ValueError, "Tag cannot be None"):
            node1.to_html()

class TestDOMTree(unittest.TestCase):
    def setUp(self):
        self.p1 = LeafNode("This is paragraph 1", "p", {"class": "p1"})
        self.p2 = LeafNode("This is paragraph 2", "p", {"class": "p2"})
        self.div_with_two_children = ParentNode([self.p1,self.p2], "div", {"class": "parent"})
        self.div_with_two_children_to_html_expected_output = "<div class=\"parent\"><p class=\"p1\">This is paragraph 1</p><p class=\"p2\">This is paragraph 2</p></div>"

        self.p3 = LeafNode("This is paragraph 3", "p", {"class": "p3"})
        self.div_with_one_parent_node_and_one_leaf_node = ParentNode([self.div_with_two_children,self.p3], "div", {"class": "grandparent"})
        self.div_with_one_parent_node_and_one_leaf_node_to_html_expected_output = "<div class=\"grandparent\"><div class=\"parent\"><p class=\"p1\">This is paragraph 1</p><p class=\"p2\">This is paragraph 2</p></div><p class=\"p3\">This is paragraph 3</p></div>"

    def test_div_with_two_children(self):
        self.assertEqual(self.div_with_two_children.to_html(), self.div_with_two_children_to_html_expected_output)
        self.assertEqual(self.div_with_two_children.to_html(), f"<div class=\"parent\">{self.p1.to_html()}{self.p2.to_html()}</div>")

    def test_div_with_one_parent_node_and_one_leaf_node(self):
        self.assertEqual(self.div_with_one_parent_node_and_one_leaf_node.to_html(), self.div_with_one_parent_node_and_one_leaf_node_to_html_expected_output)
        self.assertEqual(self.div_with_one_parent_node_and_one_leaf_node.to_html(), f"<div class=\"grandparent\">{self.div_with_two_children.to_html()}{self.p3.to_html()}</div>")


if __name__ == "__main__":
    unittest.main()