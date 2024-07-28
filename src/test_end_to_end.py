import unittest
from markdown_parser import MarkdownParser

class TestEndToEnd(unittest.TestCase):
    def setUp(self):
        self.markdown_parser = MarkdownParser()

    def test_i_like_tolkien_etc(self):
        text = "\n\n**I like Tolkien**. Read my [first post here](/majesty) (sorry the link doesn't work yet)\n\n"
        text_nodes = self.markdown_parser.parse(text)
        print(text_nodes[0])
        print(text_nodes[1])
        print(text_nodes[2])
        print(text_nodes[3])
        print(text_nodes[4])
        print(len(text_nodes[2].children))
        print(text_nodes[2].children[0])
        print(text_nodes[2].children[1])
        print(text_nodes[2].children[2])
        print(text_nodes[2].children[3])
        html_node = text_nodes[2].to_html_node()
        print(html_node.to_html())


        self.assertEqual(len(text_nodes), 3)


if __name__ == '__main__':
    unittest.main()
