from htmlnode import HTMLNode

class LeafNode(HTMLNode):

    def __init__(
            self,
            tag: str,
            value: str,
            props: dict[str: str] = None,
        ) -> None:
        super().__init__(tag, value, None, props)

    def to_html(self):
        if not self.tag:
            return self.value
        if self.tag == "img":
            return f"<{self.tag}{self.props_to_html()}>"
        if not self.value:
            #print(f"Leafnode tag = {self.tag}")
            #print(f"Leafnode value = {self.value}")
            #print(f"Leafnode props = {self.props}")
            raise ValueError("All leafnodes must have a value!")
        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"

    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, {self.props})"  
        