from textnode import TextNode, TextType
import re

def split_nodes_delimiter(old_nodes: list[TextNode], delimiter: str, text_type: TextType) -> list[TextNode]:
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type.value != "text":
            new_nodes.append(old_node)
            continue
        if old_node.text.count(delimiter) % 2 != 0:
            raise Exception(f'Error: delimiters ("{delimiter}") do not match up!')
        
        parts = old_node.text.split(delimiter)

        for i in range(len(parts)):
            if parts[i] == "":
                 continue
            elif i % 2 == 0:
                # normal text node
                new_nodes.append(TextNode(parts[i],TextType.TEXT))
            else:
                # special text node
                new_nodes.append(TextNode(parts[i], text_type))
    return new_nodes

def extract_markdown_images(text: str) -> list[tuple[str, str]]:
    # Example working:
    # text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
    # print(extract_markdown_images(text))
    # [("rick roll", "https://i.imgur.com/aKaOqIh.gif"), ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg")]
    return re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)",text)

def extract_markdown_links(text: str) -> list[tuple[str, str]]:
    # Example working:
    # text = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
    # print(extract_markdown_links(text))
    # [("to boot dev", "https://www.boot.dev"), ("to youtube", "https://www.youtube.com/@bootdotdev")]
    return re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)",text)

def split_nodes_image(old_nodes: list[TextNode]) -> list[TextNode]:
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type.value != "text":
            new_nodes.append(old_node)
            continue
        
        matches = extract_markdown_images(old_node.text)
        # If there are no image links, just append the node and continue
        if not matches:
            new_nodes.append(old_node)
            continue

        original_text = old_node.text
        for match in matches:
            image_alt = match[0]
            image_link = match[1]
            sections = original_text.split(f"![{image_alt}]({image_link})", 1)
            if sections[0] != "":
                new_nodes.append(TextNode(sections[0],TextType.TEXT))
            new_nodes.append(TextNode(image_alt,TextType.IMAGE,image_link))
            if sections[1] != "":
                original_text = sections[1]
        if sections[1] != "":
            new_nodes.append(TextNode(sections[1],TextType.TEXT))
        
    return new_nodes

def split_nodes_link(old_nodes: list[TextNode]) -> list[TextNode]:
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type.value != "text":
            new_nodes.append(old_node)
            continue
        
        matches = extract_markdown_links(old_node.text)
        # If there are no links, just append the node and continue
        if not matches:
            new_nodes.append(old_node)
            continue

        original_text = old_node.text
        for match in matches:
            link_alt = match[0]
            link_url = match[1]
            sections = original_text.split(f"[{link_alt}]({link_url})", 1)
            
            if sections[0] != "":
                new_nodes.append(TextNode(sections[0],TextType.TEXT))
            new_nodes.append(TextNode(link_alt,TextType.LINK,link_url))
            if sections[1] != "":
                original_text = sections[1]
        if sections[1] != "":
            new_nodes.append(TextNode(sections[1],TextType.TEXT))
        
    return new_nodes

def text_to_textnodes(text: str) -> list[TextNode]:
    nodes = [TextNode(text, TextType.TEXT)]
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    return nodes
