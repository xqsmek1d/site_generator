import unittest
from markdown_blocks import markdown_to_blocks, block_to_blocktype, BlockType, extract_title

class TestMarkdownBlockDivider(unittest.TestCase):
    def test_markdown_to_blocks(self):
        md = """
        This is **bolded** paragraph

        This is another paragraph with _italic_ text and `code` here
        This is the same paragraph on a new line

        - This is a list
        - with items
        """
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_markdown_to_blocks_newlines(self):
        md = """
        This is **bolded** paragraph




        This is another paragraph with _italic_ text and `code` here
        This is the same paragraph on a new line

        - This is a list
        - with items
        """
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

class TestMarkdownBlockTypeIdentifier(unittest.TestCase):
    def test_heading(self):
        md = "# This is a heading"
        block_type = block_to_blocktype(md)
        self.assertEqual(block_type, BlockType.HEADING)
    def test_code(self):
        md = "```\n asdasda \n```"
        block_type = block_to_blocktype(md)
        self.assertEqual(block_type, BlockType.CODE)
    def test_invalid_code(self):
        md = "```asdasda```"
        block_type = block_to_blocktype(md)
        self.assertEqual(block_type, BlockType.PARAGRAPH)
    def test_quote(self):
        md = "> This is a quote\n>This is also a quote"
        block_type = block_to_blocktype(md)
        self.assertEqual(block_type, BlockType.QUOTE)
    def test_invalid_quote(self):
        md = "This is not > a valid quote\n> Just like this one because it is part of the previous"
        block_type = block_to_blocktype(md)
        self.assertEqual(block_type, BlockType.PARAGRAPH)
    def test_unordered_list(self):
        md = "- This is an item\n- This is also an item"
        block_type = block_to_blocktype(md)
        self.assertEqual(block_type, BlockType.UNORDERED_LIST)
    def test_invalid_unordered_list(self):
        md = "- This is a valid item\n-This one is invalid"
        block_type = block_to_blocktype(md)
        self.assertEqual(block_type, BlockType.PARAGRAPH)
    def test_ordered_list(self):
        md = "1. This is the first item\n2. This is the second item"
        block_type = block_to_blocktype(md)
        self.assertEqual(block_type, BlockType.ORDERED_LIST)
    def test_invalid_ordered_list1(self):
        md = "1. This is the first item\n1. This is an invalid second item"
        block_type = block_to_blocktype(md)
        self.assertEqual(block_type, BlockType.PARAGRAPH)
    def test_invalid_ordered_list2(self):
        md = "1. This is the first item\n2.This is an invalid second item"
        block_type = block_to_blocktype(md)
        self.assertEqual(block_type, BlockType.PARAGRAPH)
    def test_invalid_mixed_list(self):
        md = "1. This is the first item\n- This is an invalid second item"
        block_type = block_to_blocktype(md)
        self.assertEqual(block_type, BlockType.PARAGRAPH)
    
class TestMarkdownHeadingExtractor(unittest.TestCase):
    def test_extract_simple_heading(self):
        md = "# This is the title!"
        self.assertEqual(extract_title(md), "This is the title!")

    def test_extract_simple_heading(self):
        md = """
        Suppose I have multiple lines

        # And the title is here

        Will it still extract the title?

        """
        self.assertEqual(extract_title(md), "And the title is here")

    def test_extract_simple_heading(self):
        md = """
        This is my markdown text without a title,
        
        ## It only has a second title

        ### And maybe a third

        But not a first one indicated by a leading #
        """
        self.assertEqual(extract_title(md), None)

if __name__ == "__main__":
    unittest.main()