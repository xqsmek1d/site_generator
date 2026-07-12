class HTMLNode():

    def __init__(
            self,
            tag: str = None,
            value: str = None,
            children: list[object[HTMLNode]] = None,
            props: dict[str: str] = None,
        ) -> None:

        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError

    def props_to_html(self):
        if not self.props:
            return ""

        html_props = ""
        for prop in self.props.items():
            html_props += f' {prop[0]}="{prop[1]}"'
        return html_props

    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"  