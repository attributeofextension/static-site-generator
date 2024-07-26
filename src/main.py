from textnode import TextNode
from htmlnode import LeafNode

def text_node_to_html_node(text_node):
    match text_node.text_type:
        case "text": return LeafNode(text_node.text)
        case "bold": return LeafNode(text_node.text, "b")
        case "italic": return LeafNode(text_node.text, "i")
        case "code": return LeafNode(text_node.text, "code")
        case "link": return LeafNode(text_node.text, "a", {"href": text_node.url})
        case "image": return LeafNode("", "img", {"src": text_node.url, "alt": text_node.text})
        case _:
            raise Exception("Text node type is not acceptable")

def main():
    print("hello world")
    textnode = TextNode("This is a text node", "bold", "https://www.boot.dev")
    print(textnode)

main()