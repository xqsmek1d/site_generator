from htmlnode import HTMLNode

class ParentNode(HTMLNode):

    def __init__(
            self,
            tag: str,
            children: list[object[HTMLNode]],
            props: dict[str: str] = None,
        ) -> None:
        super().__init__(tag, None, children, props)

    def to_html(self) -> str:
        if not self.tag:
            raise ValueError("All parentnodes must have a tag!")
        if not self.children:
            raise ValueError("Children are empty!")
        
        html_string = f"<{self.tag}>"
        for child in self.children:
            html_string += child.to_html()
        
        html_string += f"</{self.tag}>"
        return html_string