import unittest
from markdown_to_html_node import markdown_to_html_node

class TestMdToHTML(unittest.TestCase):
    def test_paragraphs(self):
        md = """
    This is **bolded** paragraph
    text in a p
    tag here

    This is another paragraph with _italic_ text and `code` here

    """
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_codeblock(self):
        md = """
    ```
    This is text that _should_ remain
    the **same** even with inline stuff
    ```
    """
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )
    
    def test_quoteblock(self):
        md = """
> This is **bold text** inside a quote
> and this is the second quote, but now _italic_
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><blockquote>This is <b>bold text</b> inside a quote and this is the second quote, but now <i>italic</i></blockquote></div>",
        )

    def test_unordered_list(self):
        md = """
- This is the first **bold** list item
- and this is the second list item, but now _italic_
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ul><li>This is the first <b>bold</b> list item</li><li>and this is the second list item, but now <i>italic</i></li></ul></div>",
        )

    def test_ordered_list(self):
        md = """
1. This is the first **bold** list item
2. and this is the second list item, but now _italic_
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ol><li>This is the first <b>bold</b> list item</li><li>and this is the second list item, but now <i>italic</i></li></ol></div>",
        )

if __name__ == "__main__":
    unittest.main()
