from enum import Enum
import re

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"


def markdown_to_blocks(markdown: str) -> list[str]:
    raw_blocks = markdown.split("\n\n")
    blocks = []

    for block in raw_blocks:

        if "\n" in block:
            old_block_parts = block.split("\n")
            new_block_parts = []

            for old_part in old_block_parts:
                new_block_parts.append(old_part.strip())

            block = "\n".join(new_block_parts)

        block = block.strip()

        if block == "":
            continue

        blocks.append(block)

    return blocks

# I didn't know .startswith() method before seeing the solution
def block_to_blocktype(block: str) -> BlockType:
    lines = block.split("\n")

    if block.startswith(("# ", "## ", "### ", "#### ", "##### ", "###### ")):
        return BlockType.HEADING
    if len(lines) > 1 and lines[0].startswith("```") and lines[-1].startswith("```"):
        return BlockType.CODE
    if block.startswith(">"):
        for line in lines:
            if not line.startswith(">"):
                return BlockType.PARAGRAPH
        return BlockType.QUOTE
    if block.startswith("- "):
        for line in lines:
            if not line.startswith("- "):
                return BlockType.PARAGRAPH
        return BlockType.UNORDERED_LIST
    if block.startswith("1. "):
        i = 1
        for line in lines:
            if not line.startswith(f"{i}. "):
                return BlockType.PARAGRAPH
            i += 1
        return BlockType.ORDERED_LIST
    return BlockType.PARAGRAPH 

def extract_title(markdown: str) -> str:
    markdown_lines = markdown.split("\n")
    for line in markdown_lines:
        if line.startswith("# "):
            return line[1:].strip()
    return None

'''
def block_to_blocktype(md_block: str) -> BlockType:
    md_block_lines = md_block.split("\n")

    if md_block[0] == "#":
        return BlockType.HEADING
    elif md_block[0:4] == "```\n" and md_block[-3:] == "```":
        return BlockType.CODE
    
    type_set = set()

    for count, line in enumerate(md_block_lines):

        if line == "":
            continue
        elif line[0] == ">":
            type_set.add(BlockType.QUOTE)
        elif line[0:2] == "- ":
            type_set.add(BlockType.UNORDERED_LIST)
        elif line[0:3] == f"{count+1}. ":
            type_set.add(BlockType.ORDERED_LIST)
        else:
            type_set.add(BlockType.PARAGRAPH)

    if len(type_set) == 1:
        return list(type_set)[0]

    return BlockType.PARAGRAPH 
'''