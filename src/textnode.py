class TextNode():
    def __init__(self, text, text_type, url, raw_text):
        self.text = text
        self.text_type = text_type
        self.url = url
        self.raw_text = raw_text
        self.children = []

    def __eq__(self, other):
        return self.text == other.text and self.text_type == other.text_type and self.url == other.url

    def __repr__(self):
        return f"{self.text}, {self.text_type}, {self.url}, {self.raw_text}"
