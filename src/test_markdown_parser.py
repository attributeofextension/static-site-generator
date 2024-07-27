import unittest
from markdown_parser import MarkdownParser

class TestMarkdownParser(unittest.TestCase):
    def setUp(self):
        self.markdown_parser = MarkdownParser()

    def test_line_with_bold(self):
        line = "this is a **bold** statement"
        text_nodes = self.markdown_parser.parse(line)
        self.assertEqual(len(text_nodes), 1)
        self.assertEqual(text_nodes[0].text_type, "paragraph")
        self.assertEqual(len(text_nodes[0].children),3)
        self.assertEqual(text_nodes[0].children[0].text_type, "text")
        self.assertEqual(text_nodes[0].children[1].text_type, "bold")
        self.assertEqual(text_nodes[0].children[2].text_type, "text")

    def test_line_with_italic(self):
        line = "this is a *italic* statement"
        text_nodes = self.markdown_parser.parse(line)
        self.assertEqual(len(text_nodes), 1)
        self.assertEqual(text_nodes[0].text_type, "paragraph")
        self.assertEqual(len(text_nodes[0].children),3)
        self.assertEqual(text_nodes[0].children[0].text_type, "text")
        self.assertEqual(text_nodes[0].children[1].text_type, "italic")
        self.assertEqual(text_nodes[0].children[2].text_type, "text")

    def test_line_with_code(self):
        line = "this is a `code` statement"
        text_nodes = self.markdown_parser.parse(line)
        self.assertEqual(len(text_nodes), 1)
        self.assertEqual(text_nodes[0].text_type, "paragraph")
        self.assertEqual(len(text_nodes[0].children),3)
        self.assertEqual(text_nodes[0].children[0].text_type, "text")
        self.assertEqual(text_nodes[0].children[1].text_type, "code")
        self.assertEqual(text_nodes[0].children[2].text_type, "text")

    def test_line_with_image(self):
        line = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        text_nodes = self.markdown_parser.parse(line)
        self.assertEqual(len(text_nodes), 1)
        self.assertEqual(text_nodes[0].text_type, "paragraph")
        self.assertEqual(len(text_nodes[0].children),3)
        self.assertEqual(text_nodes[0].children[0].text_type, "text")
        self.assertEqual(text_nodes[0].children[1].text_type, "image")
        self.assertEqual(text_nodes[0].children[1].text, "rick roll")
        self.assertEqual(text_nodes[0].children[1].url, "https://i.imgur.com/aKaOqIh.gif")
        self.assertEqual(text_nodes[0].children[2].text_type, "text")
        self.assertEqual(len(text_nodes[0].children[2].children), 2)
        self.assertEqual(text_nodes[0].children[2].children[0].text_type, "text")
        self.assertEqual(text_nodes[0].children[2].children[0].text, " and ")
        self.assertEqual(text_nodes[0].children[2].children[1].text_type, "image")
        self.assertEqual(text_nodes[0].children[2].children[1].text, "obi wan")
        self.assertEqual(text_nodes[0].children[2].children[1].url, "https://i.imgur.com/fJRm4Vk.jpeg")

if __name__ == '__main__':
    unittest.main()
