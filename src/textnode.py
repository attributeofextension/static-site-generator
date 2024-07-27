from htmlnode import HTMLNode, ParentNode, LeafNode

class TextNode():
    def __init__(self, text, text_type, url=None, raw_text=None):
        self.text = text
        self.text_type = text_type
        self.url = url
        self.raw_text = raw_text
        self.children = []

    def __eq__(self, other):
        return self.text == other.text and self.text_type == other.text_type and self.url == other.url

    def __str__(self):
        return f"({self.raw_text}, {len(self.children)})\n"

    def __get_html_tag(self):
        match self.text_type:
            case "h1": return "h1"
            case "h2": return "h2"
            case "h3": return "h3"
            case "h4": return "h4"
            case "h5": return "h5"
            case "paragraph": return "p"
            case "bold": return "b"
            case "italic": return "i"
            case "link": return "a"
            case "image": return "img"
            case "ul": return "ul"
            case "ol": return "ol"
            case "ul-item": return "li"
            case "ol-item": return "li"
            case "code-block": return "code"
            case "code": return "code"
            case "quote": return "blockquote"
            case "text": return ""
            case _:
                return None

    def __get_html_tag_props(self):
        match self.text_type:
            case "image": return {"src": self.url, "alt":self.text}
            case "link": return {"href": self.url}
            case _:
                return None

    def can_covert_to_html_node(self):
        return self.__get_html_tag() is not None

    def can_convert_to_parent_node(self):
        if len(self.children) == 0:
            return False

        match self.text_type:
            case "text": return False
            case "link": return False
            case "code": return False
            case "code-block": return False
            case "quote": return False
            case "image": return False
            case _:
                return True


    def to_html_node(self):
        if not self.can_covert_to_html_node():
            raise Exception(f"Can't convert text-type: {self.text_type} to HTML node")
        if len(self.children) > 0 and self.can_convert_to_parent_node():
            inner_html_nodes = []
            for child in self.children:
                if self.text_type == "ul" and child.text_type != "ul-item":
                    raise Exception(f"Invalid child text_type ({child.text_type}) for text_type: {self.text_type}")
                if self.text_type == "ol" and child.text_type != "ol-item":
                    raise Exception(f"Invalid child text_type ({child.text_type}) for text_type: {self.text_type}")

                if child.can_covert_to_html_node():
                    try:
                        html_node = child.to_html_node()
                        inner_html_nodes.append(child.to_html_node())
                    except Exception as e:
                        print(e)
                        continue
            return ParentNode(inner_html_nodes, self.__get_html_tag(), self.__get_html_tag_props())
        else:
            if self.text_type == "ul":
                raise Exception("Can't convert text-type:ul to HTML node if it has no children")
            if self.text_type == "ol":
                raise Exception("Can't convert text-type:ol to HTML node if it has no children")

            match self.text_type:
                case "image": return LeafNode(None, self.__get_html_tag(), self.__get_html_tag_props())
                case "link": return LeafNode(self.text, self.__get_html_tag(), self.__get_html_tag_props())
                case "code-block":
                    code_node = LeafNode(self.text, self.__get_html_tag(), self.__get_html_tag_props())
                    return ParentNode([code_node], "pre", None)
                case _:
                    return LeafNode(self.text, self.__get_html_tag(), self.__get_html_tag_props())

