from htmlnode import HTMLNode
from textnode import TextNode, TextType, text_node_to_html_node
from markdown_blocks import markdown_to_blocks, block_to_blocktype, BlockType
from inline_markdown import text_to_textnodes
from parentnode import ParentNode

def text_to_children(text): 
    text_nodes = text_to_textnodes(text)
    html_nodes = []
    for text_node in text_nodes:
        html_nodes.append(text_node_to_html_node(text_node))
    return html_nodes

def markdown_to_html_node(markdown: str) ->  HTMLNode:
    markdown_blocks = markdown_to_blocks(markdown)
    block_nodes = []

    for md_block in markdown_blocks:
        block_type = block_to_blocktype(md_block)

        if block_type.value == "paragraph":
            #Extract the actual text content from md_block (stripping markdown syntax like #, >, -, 1., etc.)
                # Not needed for a paragraph

            #Call text_to_children on that text to get the inline children
            children = text_to_children(md_block.replace("\n"," "))

            #Wrap those children in the appropriate tag (per your Tips section)
            parent = ParentNode("p",children)

            #Append the resulting node to block_nodes
            block_nodes.append(parent)

        elif block_type.value == "heading":
            #Extract the actual text content from md_block (stripping markdown syntax like #, >, -, 1., etc.)
                # Handled in the next line by the lstrip method, but we need to get the amount of #:
            h_count = len(md_block) - len(md_block.lstrip("#"))
            if h_count < 1 or h_count > 6:
                raise Exception("Error: invalid heading used")

            #Call text_to_children on that text to get the inline children
            children = text_to_children(md_block[h_count+1:].replace("\n"," "))

            #Wrap those children in the appropriate tag (per your Tips section)
            parent = ParentNode(f"h{h_count}",children)

            #Append the resulting node to block_nodes
            block_nodes.append(parent)

        elif block_type.value == "code":
            md_block = md_block[4:-3]
            text_node = TextNode(md_block, TextType.CODE)
            code_node = text_node_to_html_node(text_node)
            html_node = ParentNode("pre",[code_node])
            block_nodes.append(html_node)

        elif block_type.value == "quote":
            block_lines = md_block.split("\n")
            new_md_block = []
            for line in block_lines:
                if line.startswith("> "):
                    new_md_block.append(line[2:].strip())
                elif line.startswith(">"):
                    new_md_block.append(line[1:].strip())
                else:
                    raise Exception("Error: quotes formatted incorrectly")
            md_block = "\n".join(new_md_block)

            children = text_to_children(md_block.replace("\n"," "))

            parent = ParentNode("blockquote",children)

            block_nodes.append(parent)

        elif block_type.value == "unordered_list":
            block_lines = md_block.split("\n")
            children = []

            for line in block_lines:
                if line.startswith("- "):
                    grandchildren = text_to_children(line[2:].strip())
                    child = ParentNode("li",grandchildren)
                    children.append(child)
                else:
                    raise Exception("Error: ulist formatted incorrectly")

            parent = ParentNode("ul",children)

            block_nodes.append(parent)

        elif block_type.value == "ordered_list":
            block_lines = md_block.split("\n")
            children = []

            for index,line in enumerate(block_lines):
                count = index + 1
                if line.startswith(f"{count}. "):
                    grandchildren = text_to_children(line[len(str(count))+2:].strip())
                    child = ParentNode("li",grandchildren)
                    children.append(child)
                else:
                    raise Exception("Error: olist formatted incorrectly")

            parent = ParentNode("ol",children)

            block_nodes.append(parent)

        else:
            raise Exception("Error: somehow the block type has gone wrong for a markdown block!")

    main_node = ParentNode("div",block_nodes)
    return main_node
    