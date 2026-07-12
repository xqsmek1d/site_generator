from enum import Enum
from leafnode import LeafNode

class TextType(Enum):
    TEXT = "text"
    BOLD = "bold"
    ITALIC = "italic"
    CODE = "code"
    LINK = "link"
    IMAGE = "image"

class TextNode():

    def __init__(self, text: str, text_type: object(TextType), url: str = None) -> None:
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, other: object(TextNode)) -> bool:
        if (
            self.text == other.text and
            self.text_type == other.text_type and
            self.url == other.url
        ):
            return True
        else:
            return False

    def __repr__(self) -> str:
        return f"TextNode({self.text}, {self.text_type.value}, {self.url})"  
    
def text_node_to_html_node(text_node: TextNode) -> LeafNode:
    text = text_node.text
    match text_node.text_type.value:
        case "text":
            return LeafNode(None,text)
        case "bold":
            return LeafNode("b",text)
        case "italic":
            return LeafNode("i",text)
        case "code":
            return LeafNode("code",text)
        case "link":
            return LeafNode("a",text,{"href":text_node.url})
        case "image":
            return LeafNode("img","",{"src":text_node.url, "alt":text})
        case _:
            raise Exception("Error: invalid text type")

