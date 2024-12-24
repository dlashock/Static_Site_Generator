from enum import Enum

class TextType(Enum):
    NORMAL = "normal"
    BOLD = "bold"
    ITALIC = "italic"
    CODE = "code"
    LINKS = "links"
    IMAGES = "images"

class TextNode:
    def __init__(self, text, text_type, url=None):
        self.text = text
        
        match text_type:
            case "normal" | TextType.NORMAL:
                self.text_type = TextType.NORMAL
            case "bold" | TextType.BOLD:
                self.text_type = TextType.BOLD
            case "italic" | TextType.ITALIC:
                self.text_type = TextType.ITALIC
            case "code" | TextType.CODE:
                self.text_type = TextType.CODE
            case "links" | TextType.LINKS:
                self.text_type = TextType.LINKS
            case "images" | TextType.IMAGES:
                self.text_type = TextType.IMAGES
            case _:
                raise Exception("Invalid text type")

        self.url = url

    def __eq__(self, other):
        return  (self.text == other.text and 
                self.text_type == other.text_type and
                self.url == other.url)

    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type.value}, {self.url})"