from textnode import TextNode
from htmlnode import LeafNode
from shutil import rmtree, copy
from os import path, listdir, mkdir


# deprecated
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

def copy_tree(src, dst):
    contents = listdir(src)
    for content in contents:
        if path.isfile(path.join(src, content)):
            print(f"Copying {path.join(src, content)} to {path.join(dst, content)}")
            copy(path.join(src, content), path.join(dst, content))
        elif path.exists(path.join(src, content)):
            mkdir(path.join(dst, content))
            copy_tree(path.join(src, content), path.join(dst, content))



def deploy_static_assets_to_public():
    # clean public/
    if path.exists("public"):
        rmtree("public")
        mkdir("public")

    if not path.exists("static"):
        raise Exception("Static assets directory does not exist")
    copy_tree("static", "public")








def main():
    deploy_static_assets_to_public()


main()