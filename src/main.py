from textnode import TextNode
from htmlnode import LeafNode
from shutil import rmtree, copy
from os import path, listdir, mkdir
import re
from markdown_parser import MarkdownParser

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
        if content.endswith(".html"):
            continue
        if content == "content":
            continue
        if path.isfile(path.join(src, content)):
            print(f"Copying {path.join(src, content)} to {path.join(dst, content)}")
            copy(path.join(src, content), path.join(dst, content))
        elif path.isdir(path.join(src, content)):
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

def extract_title(markdown: str) -> str:
    first_line_regex = re.compile(r"# .*?\n")
    anywhere_else_regex = re.compile(r"\n# *.?\n")
    if markdown.startswith("# "):
        if re.search(r"\n", markdown) is None:
            return markdown[2:]
        else:
            results = re.search(first_line_regex, markdown)
            if results is not None:
                return results[0][2:-1]
    else:
        results = re.search(anywhere_else_regex, markdown)
        if results is not None:
            return results[0][3:-1]
    raise Exception("No h1 header found")

def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    markdown = open(from_path, "r").read()
    title = extract_title(markdown)
    markdown_parser = MarkdownParser()
    text_nodes = markdown_parser.parse(markdown)
    html_nodes = list(map(lambda x: x.to_html_node(), text_nodes))

    article_html = "\n".join(list(map(lambda x: x.to_html(), html_nodes)))

    template = open(template_path, "r").read()
    title_regex = re.compile(r"\{\{ Title }}")
    content_regex = re.compile(r"\{\{ Content }}")
    index_html = title_regex.sub(title, template)
    index_html = content_regex.sub(article_html, index_html)

    if path.isfile(dest_path):
        open(dest_path, "w").write(index_html)
    else:
        open(dest_path, "x").write(index_html)

def generate_pages_recursive(dir_path_content: str, template_path: str, dest_dir_path: str):
    current_dir_contents = listdir(dir_path_content)

    for dir_content in current_dir_contents:
        create_path = re.sub(r"content/","", dir_content)
        if path.isdir(path.join(dir_path_content, dir_content)):
            if not path.isdir(path.join(dest_dir_path, create_path)):
                mkdir(path.join(dest_dir_path, create_path))
            generate_pages_recursive(path.join(dir_path_content, dir_content), template_path, path.join(dest_dir_path, create_path))
        elif path.isfile(path.join(dir_path_content, dir_content)):
            filename = ".".join(dir_content.split(".")[:-1] + ["html"])

            generate_page(path.join(dir_path_content, dir_content), template_path, path.join(dest_dir_path, filename))

def main():
    deploy_static_assets_to_public()
    generate_pages_recursive(path.join("static", "content"), path.join("static", "template.html"), path.join("public"))

main()