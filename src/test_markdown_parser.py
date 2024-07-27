import unittest
from markdown_parser import MarkdownParser
from src.textnode import TextNode


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
        self.assertEqual(len(text_nodes[0].children),4)
        self.assertEqual(text_nodes[0].children[0].text_type, "text")
        self.assertEqual(text_nodes[0].children[1].text_type, "image")
        self.assertEqual(text_nodes[0].children[1].text, "rick roll")
        self.assertEqual(text_nodes[0].children[1].url, "https://i.imgur.com/aKaOqIh.gif")
        self.assertEqual(text_nodes[0].children[2].text_type, "text")
        self.assertEqual(text_nodes[0].children[2].text, " and ")
        self.assertEqual(text_nodes[0].children[3].text_type, "image")
        self.assertEqual(text_nodes[0].children[3].text, "obi wan")
        self.assertEqual(text_nodes[0].children[3].url, "https://i.imgur.com/fJRm4Vk.jpeg")

    def test_line_from_step_3_6_text_to_text_node(self):
        line = "This is **text** with an *italic* word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        text_nodes = self.markdown_parser.parse(line)
        self.assertEqual(len(text_nodes), 1)

        self.assertEqual(text_nodes[0].text_type, "paragraph")
        self.assertEqual(len(text_nodes[0].children), 10)

        self.assertEqual(text_nodes[0].children[0].text_type, "text")
        self.assertEqual(text_nodes[0].children[0].text, "This is ")

        self.assertEqual(text_nodes[0].children[1].text_type, "bold")
        self.assertEqual(text_nodes[0].children[1].text, "text")

        self.assertEqual(text_nodes[0].children[2].text_type, "text")
        self.assertEqual(text_nodes[0].children[2].text, " with an ")

        self.assertEqual(text_nodes[0].children[3].text_type, "italic")
        self.assertEqual(text_nodes[0].children[3].text, "italic")

        self.assertEqual(text_nodes[0].children[4].text_type, "text")
        self.assertEqual(text_nodes[0].children[4].text, " word and a ")

        self.assertEqual(text_nodes[0].children[5].text_type, "code")
        self.assertEqual(text_nodes[0].children[5].text, "code block")

        self.assertEqual(text_nodes[0].children[6].text_type, "text")
        self.assertEqual(text_nodes[0].children[6].text, " and an ")

        self.assertEqual(text_nodes[0].children[7].text_type, "image")
        self.assertEqual(text_nodes[0].children[7].text, "obi wan image")
        self.assertEqual(text_nodes[0].children[7].url, "https://i.imgur.com/fJRm4Vk.jpeg")

        self.assertEqual(text_nodes[0].children[8].text_type, "text")
        self.assertEqual(text_nodes[0].children[8].text, " and a ")

        self.assertEqual(text_nodes[0].children[9].text_type, "link")
        self.assertEqual(text_nodes[0].children[9].text, "link")
        self.assertEqual(text_nodes[0].children[9].url, "https://boot.dev")

    def test_block_from_step_4_1_blocks_split_blocks(self):
        block = "# This is a heading\nThis is a paragraph of text. It has some **bold** and *italic* words inside of it.\n* This is the first list item in a list block\n* This is a list item\n* This is another list item"

        text_nodes = self.markdown_parser.parse(block)

        self.assertEqual(len(text_nodes), 3)

        self.assertEqual(text_nodes[0].text_type, "h1")
        self.assertEqual(text_nodes[0].text, "This is a heading")

        self.assertEqual(text_nodes[1].text_type, "paragraph")
        self.assertEqual(text_nodes[1].text, "This is a paragraph of text. It has some **bold** and *italic* words inside of it.")
        self.assertEqual(len(text_nodes[1].children), 5)

        self.assertEqual(text_nodes[1].children[0].text_type, "text")
        self.assertEqual(text_nodes[1].children[0].text, "This is a paragraph of text. It has some ")

        self.assertEqual(text_nodes[1].children[1].text_type, "bold")
        self.assertEqual(text_nodes[1].children[1].text, "bold")

        self.assertEqual(text_nodes[1].children[2].text_type, "text")
        self.assertEqual(text_nodes[1].children[2].text, " and ")

        self.assertEqual(text_nodes[1].children[3].text_type, "italic")
        self.assertEqual(text_nodes[1].children[3].text, "italic")

        self.assertEqual(text_nodes[1].children[4].text_type, "text")
        self.assertEqual(text_nodes[1].children[4].text, " words inside of it.")

        self.assertEqual(text_nodes[2].text_type, "ul")
        self.assertEqual(text_nodes[2].text, "")
        self.assertEqual(text_nodes[2].raw_text, "* This is the first list item in a list block\n* This is a list item\n* This is another list item")

        self.assertEqual(text_nodes[2].children[0].text_type, "ul-item")
        self.assertEqual(text_nodes[2].children[0].text, "This is the first list item in a list block")

        self.assertEqual(text_nodes[2].children[1].text_type, "ul-item")
        self.assertEqual(text_nodes[2].children[1].text, "This is a list item")

        self.assertEqual(text_nodes[2].children[2].text_type, "ul-item")
        self.assertEqual(text_nodes[2].children[2].text, "This is another list item")



if __name__ == '__main__':
    unittest.main()
