from typing import Match, List, Tuple
from textnode import TextNode
import re
from functools import reduce

class PerStringRule():
    def apply(self, text: str) -> list[TextNode|str]:
        pass

class PerListRule():
    def apply_to_list(self, text_nodes_and_strings: list[TextNode|str]) -> list[TextNode|str]:
        pass

class SanitizeRule(PerStringRule):
    def apply(self, text: str) -> list[TextNode|str]:
        regex_open = re.compile(r"<.*?script*.?>")
        regex_close = re.compile(r"</.*?script.*?>")

        sanitized_text = regex_open.sub("", text)
        sanitized_text = regex_close.sub("", sanitized_text)

        return [sanitized_text]


# breaks markdown into either chunks or lines or code segments
class BreakPerStringIntoBlocksRule(PerStringRule):
    def __mapping_function(self, text: str) -> str | TextNode:
        if text[0:3] == "```" and text[-3:] == "```":
            return TextNode(text[3:-3], "code-block", None, text )
        elif text[0:2] == "* ":
            return TextNode(text[2:], "ul-item", None, text )
        else:
            ol_item_match = re.match(rf"\d{re.escape(".")}", text)
            if ol_item_match is not None:
                return TextNode(text[3:], "ol-item", None, text )
        return text

    def apply(self, text: str) -> list[TextNode|str]:
        blocks: list[str] = re.split(r"```.*?```", text, flags=re.DOTALL)
        all_blocks = []
        if len(blocks) > 1:
            for i in range(0, len(blocks)):
                code_block = re.search(r"```.*?```", text, flags=re.DOTALL)
                if code_block is not None:
                    text = re.sub(r"```.*?```", "", text, flags=re.DOTALL)
                    all_blocks.append(blocks[i])
                    all_blocks.append(code_block[0])
                else:
                    all_blocks.append(blocks[i])

        return list(map(self.__mapping_function, list(filter(lambda x: len(x) > 0, all_blocks))))

class GroupListItemIntoBlocksRule(PerListRule):
    def __init__(self, item_text_type: str, list_text_type: str):
        self.item_text_type = item_text_type
        self.list_text_type = list_text_type

    def __group_list_items_into_block(self, markdown_list: list[TextNode]) -> TextNode:
        raw_text: str = "\n".join(map(lambda x: x.raw_text, markdown_list))
        text_node = TextNode("", self.list_text_type, None, raw_text)
        text_node.children = list(markdown_list)
        return text_node

    def apply_to_list(self, text_nodes_and_strings: list[TextNode|str]) -> list[TextNode|str]:
        text_nodes_and_strings_copy = text_nodes_and_strings.copy()

        markdown_list = None
        for i in range(len(text_nodes_and_strings)-1, -1, -1):
            status_is_instance = isinstance(text_nodes_and_strings[i], TextNode)
            status_text_type = text_nodes_and_strings[i].text_type == self.list_text_type
            status_list_is_not_noe = markdown_list is not None
            text_type = text_nodes_and_strings[i].text_type
            if isinstance(text_nodes_and_strings[i], TextNode) and text_nodes_and_strings[i].text_type == self.item_text_type and markdown_list is None:
                markdown_list = [text_nodes_and_strings[i]]
            elif isinstance(text_nodes_and_strings[i], TextNode) and text_nodes_and_strings[i].text_type == self.item_text_type and markdown_list is not None:
                markdown_list.insert(0, text_nodes_and_strings[i])
            else:
                if markdown_list is not None:
                    block_node = self.__group_list_items_into_block(markdown_list)
                    text_nodes_and_strings_copy = text_nodes_and_strings_copy[0:i+1] + [block_node] + text_nodes_and_strings_copy[i+len(markdown_list)+2:]
                    markdown_list = None

        return text_nodes_and_strings_copy


class BreakBlocksIntoLinesRule(PerStringRule):
    def apply(self, text: str) -> list[TextNode|str]:
        lines: list[str] = text.split("\n")

        return lines

class StartOfLineRule(PerStringRule):
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
                return [TextNode(text[3:], "ol-item", None, text)]
        return [TextNode(text, "paragraph", None, text)]

class NestedRule(PerStringRule):
    def __mapping_function(self, text: str) -> str | TextNode:
        if text.startswith("**"):
            return TextNode(text[2:-2], "bold", None, text)
        elif text.startswith("*"):
            return TextNode(text[1:-1], "italic", None, text)
        elif text.startswith("`"):
            return TextNode(text[1:-1], "code", None, text)
        elif text.startswith("[link]"):
            return TextNode(text[2:-1], "link", None, text)
        else:
            return TextNode(text, "text", None, text)

    def apply(self, text: str) -> list[TextNode]:
        lookup = {
            "**": re.compile(f"{re.escape("**")}.*?{re.escape("**")}"),
            "*": re.compile(f"{re.escape("*")}.*?{re.escape("*")}"),
            "`": re.compile(f"`.*?`"),
            "!": [
                re.compile(r"\!\[.*?\]\(.*?\.(jpg|gif|jpeg|png)\)"),
                re.compile(r"\!\[.*?\]"),
                re.compile(r"\(.*?\.(jpg|gif|jpeg|png)\)")
            ],
            "[": [
                re.compile(r"\[.*?\]\(.*?\)"),
                re.compile(r"\[.*?\]"),
                re.compile(r"\(.*?\)"),
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
                        text[i+len(match[0]):]
                    ]))))
                else:
                    continue
            elif text[i:].startswith("`"):
                match = re.match(lookup["`"], text[i:])
                if match is not None:
                    return list(map(self.__mapping_function, list(filter(lambda x: len(x) > 0, [
                        text[0:i],
                        text[i:i+len(match[0])],
                        text[i+len(match[0]):]
                    ]))))
                else:
                    continue
            elif text[i:].startswith("["):
                match = re.match(lookup["["][0], text[i:])
                if match is not None:
                    link_text = re.search(lookup["["][1], match[0])
                    url = re.search(lookup["["][2], match[0])
                    return list(filter(lambda x: len(x.text) > 0, [
                        TextNode(text[0:i], "text", None, text[0:i]),
                        TextNode(link_text[0][1:-1], "link", url[0][1:-1], match[0]),
                        TextNode(text[i+len(match[0]):], "text", None, text[len(match[0]):])
                    ]))
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
        self.sanitize_rule = SanitizeRule()
        self.block_rule = BreakPerStringIntoBlocksRule()
        self.line_rule = BreakBlocksIntoLinesRule()
        self.group_ol_items_rule = GroupListItemIntoBlocksRule("ol-item", "ol")
        self.group_ul_items_rule = GroupListItemIntoBlocksRule("ul-item", "ul")
        self.start_of_line_rule = StartOfLineRule()
        self.nested_rule = NestedRule()

    def __map_block_to_line_rule_apply_results(self, block: TextNode | str) -> list[str]:
        if isinstance(block, TextNode):
            return [block]
        else:
            return self.line_rule.apply(block)

    def __map_line_to_start_of_line_rule(self, line: TextNode | str) -> list[TextNode]:
        if isinstance(line, TextNode):
            return [line]
        else:
            return self.start_of_line_rule.apply(line)

    def __search_for_text_node_with_children_and_replace_with_children(self, text_node: TextNode) -> list[TextNode]:
        if isinstance(text_node, str):
            raise ValueError(f"Unexpected unprocessed string: {text_node}")
        if len(text_node.children) > 0:
            children_copy = list(text_node.children)
            for i in range(0, len(text_node.children)):
                grandchildren = self.__search_for_text_node_with_children_and_replace_with_children(text_node.children[i])
                if len(grandchildren) > 1:
                    children_copy = children_copy[:i] + grandchildren + children_copy[i+1:]
            text_node.children = children_copy

            if text_node.text_type == "text":
                return text_node.children
            else:
                return [text_node]
        else:
            return [text_node]

    def __expand_text_node(self, text_node: TextNode) -> TextNode:
        if len(text_node.children) > 0:
            new_children = []
            for child in text_node.children:
                new_children.append(self.__expand_text_node(child))
            text_node.children = new_children
            return text_node
        children = self.nested_rule.apply(text_node.text)
        if len(children) == 1 and children[0].text == text_node.text:
            return text_node
        else:
            for child in children:
                text_node.children.append(self.__expand_text_node(child))
            return text_node

    def parse(self, text: str) -> list[TextNode]:
        sanitized_text = self.sanitize_rule.apply(text)[0]
        text_nodes: list[TextNode|str] = self.block_rule.apply(sanitized_text)
        text_nodes = list(reduce(lambda a,b: a + b, list(map(self.__map_block_to_line_rule_apply_results, text_nodes))))
        text_nodes = list(reduce(lambda a,b: a + b, list(map(self.__map_line_to_start_of_line_rule, text_nodes))))
        text_nodes = self.group_ol_items_rule.apply_to_list(text_nodes)
        text_nodes = self.group_ul_items_rule.apply_to_list(text_nodes)


        for text_node in text_nodes:
            if isinstance(text_node, TextNode) and text_node.text_type == "code":
                continue
            if isinstance(text_node, TextNode):
                self.__expand_text_node(text_node)
            else:
                raise ValueError(f"Unexpected unprocessed string: {text_node}")

        text_nodes_copy = list(text_nodes)
        for i in range(0, len(text_nodes)):
            if isinstance(text_nodes_copy[i], str):
                raise ValueError(f"Unexpected unprocessed string: {text_nodes_copy[i]}")

            if isinstance(text_nodes[i], TextNode):
                potential_split = self.__search_for_text_node_with_children_and_replace_with_children(text_nodes[i])
                if len(potential_split) > 1:
                    text_nodes_copy = text_nodes_copy[:i] + potential_split + text_nodes_copy[i+1:]

        return text_nodes_copy