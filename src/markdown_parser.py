from typing import Match, List, Tuple
from textnode import TextNode
import re
from functools import reduce

class MarkdownRule():
    def apply(self, text: str) -> list[TextNode|str]:
        pass

# breaks markdown into either chunks or lines or code segments
class BreakMarkdownIntoBlocksRule(MarkdownRule):
    def __mapping_function(self, text: str) -> str | TextNode:
        if text[0:3] == "```" and text[-3:] == "```":
            return TextNode(text[3,-3], "code-block", None, text )
        else:
            return text

    def apply(self, text: str) -> list[TextNode|str]:
        blocks: list[str] = re.split("```(.*)```", text, flags=re.DOTALL)

        return list(map(self.__mapping_function, list(filter(lambda x: len(x) > 0, blocks))))

class BreakBlocksIntoLinesRule(MarkdownRule):
    def apply(self, text: str) -> list[TextNode|str]:
        lines: list[str] = text.split("\n")

        return lines

class StartOfLineRule(MarkdownRule):
    def apply(self, text: str) -> list[TextNode|str]:
        text_type = None
        image_match = None
        ol_item_match = None
        if text.startswith("##### "):
            return [TextNode(text[6:], "h1", None, text)]
        elif text.startswith("#### "):
            return [TextNode(text[5:], "h2", None, text)]
        elif text.startswith("### "):
            return [TextNode(text[4:], "h3", None, text)]
        elif text.startswith("## "):
            return [TextNode(text[3:], "h2", None, text)]
        elif text.startswith("# "):
            return [TextNode(text[2:], "h1", None, text)]
        elif text.startswith("* "):
            return [TextNode(text[2:], "ul-item", None, text)]
        elif text.startswith("> "):
            return [TextNode(text[2:], "quote", None, text)]
        else:
            ol_item_match = re.match(rf"\d{re.escape(".")}", text)
            if ol_item_match is not None:
                return [TextNode(ol_item_match[1], "ol-item", None, text)]
        return [TextNode(text, "paragraph", None, text)]

class NestedRule(MarkdownRule):
    def __mapping_function(self, text: str) -> str | TextNode:
        if text.startswith("**"):
            return TextNode(text[2:-2], "bold", None, text)
        elif text.startswith("*"):
            return TextNode(text[1:-1], "italic", None, text)
        elif text.startswith("`"):
            return TextNode(text[1:-1], "code", None, text)
        else:
            return TextNode(text, "text", None, text)

    def apply(self, text: str) -> list[TextNode]:
        lookup = {
            "**": re.compile(f"{re.escape("**")}.*{re.escape("**")}"),
            "*": re.compile(f"{re.escape("*")}.*{re.escape("*")}"),
            "`": re.compile(f"`.*`"),
            "!": [
                re.compile(r"\!\[.*?\]\(.*?\.(jpg|gif|jpeg|png)\)"),
                re.compile(r"\!\[.*?\]"),
                re.compile(r"\(.*?\.(jpg|gif|jpeg|png)\)")
            ]
        }
        match = None
        for i in range(0, len(text)):
            if text[i:].startswith("**"):
                match = re.match(lookup["**"], text[i:])
                if match is not None:
                    return list(map(self.__mapping_function,list(filter(lambda x: len(x) > 0,[
                        text[0:i],
                        text[i:i+len(match[0])],
                        text[i+len(match[0]):]
                    ]))))
                else:
                    continue
            elif text[i:].startswith("*"):
                match = re.search(lookup["*"], text[i:])
                if match is not None:
                    return list(map(self.__mapping_function, list(filter(lambda x: len(x) > 0, [
                        text[0:i],
                        text[i:i+len(match[0])],
                        text[len(match[0]):]
                    ]))))
                else:
                    continue
            elif text[i:].startswith("`"):
                match = re.match(lookup["`"], text[i:])
                if match is not None:
                    return list(map(self.__mapping_function, list(filter(lambda x: len(x) > 0, [
                        text[0:i],
                        text[i:i+len(match[0])],
                        text[len(match[0]):]
                    ]))))
                else:
                    continue
            elif text[i:].startswith("!"):
                match = re.search(lookup["!"][0], text[i:])
                if match is not None:
                    alt_text = re.search(lookup["!"][1], match[0])
                    img_url = re.search(lookup["!"][2], match[0])
                    return list(filter(lambda x: len(x.text) > 0, [
                        TextNode(text[0:i], "text", None, text[0:i]),
                        TextNode(alt_text[0][2:-1], "image", img_url[0][1:-1],match[0]),
                        TextNode(text[i+len(match[0]):], "text", None, text[len(match[0]):])
                    ]))
                else:
                    continue
        return [TextNode(text, "text", None, text)]

class MarkdownParser():
    def __init__(self):
        self.block_rule = BreakMarkdownIntoBlocksRule()
        self.line_rule = BreakBlocksIntoLinesRule()
        self.start_of_line_rule = StartOfLineRule()
        self.nested_rule = NestedRule()

    def __map_block_to_line_rule_apply_results(self, block: TextNode | str) -> list[str]:
        if isinstance(block, TextNode):
            return block
        else:
            return self.line_rule.apply(block)

    def __map_line_to_start_of_line_rule(self, line: TextNode | str) -> list[TextNode]:
        if isinstance(line, TextNode):
            return line
        else:
            return self.start_of_line_rule.apply(line)

    def __expand_text_node(self, text_node: TextNode) -> TextNode:
        children = self.nested_rule.apply(text_node.text)
        if len(children) == 1 and children[0].text == text_node.text:
            return text_node
        else:
            for child in children:
                text_node.children.append(self.__expand_text_node(child))
            return text_node

    def parse(self, text: str):
        text_nodes: list[TextNode|str] = self.block_rule.apply(text)
        text_nodes = list(reduce(lambda a,b: a + b, list(map(self.__map_block_to_line_rule_apply_results, text_nodes))))
        text_nodes = list(reduce(lambda a,b: a + b, list(map(self.__map_line_to_start_of_line_rule, text_nodes))))

        for text_node in text_nodes:
            if isinstance(text_node, TextNode) and text_node.text_type == "code":
                continue
            if isinstance(text_node, TextNode):
                self.__expand_text_node(text_node)
            else:
                raise ValueError(f"Unexpected unprocessed string: {text_node}")

        return text_nodes