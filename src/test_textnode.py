import unittest
from textnode import TextNode, TextType, text_node_to_html_node
from inline_markdown import split_nodes_delimiter, extract_markdown_images, extract_markdown_links, split_nodes_image, split_nodes_link, text_to_textnodes

class TestTextNode(unittest.TestCase):

    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_noneq_text(self):
        node = TextNode("This is a TextNode", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertNotEqual(node, node2)

    def test_noneq_text_type(self):
        node = TextNode("This is a text node", TextType.ITALIC)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertNotEqual(node, node2)

    def test_noneq_url(self):
        node = TextNode("This is a text node", TextType.LINK, "https://www.boot.dev")
        node2 = TextNode("This is a text node", TextType.LINK, "https://www.youtube.com")
        self.assertNotEqual(node, node2)

    def test_none_url(self):
        node = TextNode("This is a TextNode", TextType.BOLD)
        self.assertIsNone(node.url)

class TestTextToHTML(unittest.TestCase):
    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_bold(self):
        node = TextNode("This is a bold text node", TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "This is a bold text node")

    def test_link(self):
        node = TextNode("This is a link text node", TextType.LINK, "https://www.boot.dev/lessons/80ddb6c5-8324-4850-a28c-0c6207596857")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "This is a link text node")
        self.assertEqual(html_node.props, {"href": "https://www.boot.dev/lessons/80ddb6c5-8324-4850-a28c-0c6207596857"})
        

    def test_image(self):
        node = TextNode("This is an image text node", TextType.IMAGE, "https://share.google/JFCgcIDpTTzqtbcUe")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, "")
        self.assertEqual(html_node.props, {"src":"https://share.google/JFCgcIDpTTzqtbcUe", "alt": "This is an image text node"})

class TestTextSplitDelimiter(unittest.TestCase):
    def test_nothing(self):
        old_node = TextNode("This is a text node", TextType.TEXT)
        new_nodes = split_nodes_delimiter([old_node], "`", TextType.CODE)
        self.assertEqual(new_nodes[0].text, "This is a text node")
        self.assertEqual(new_nodes[0].text_type.value, "text")

    def test_single_split(self):
        old_node = TextNode("This is a `code` node", TextType.TEXT)
        new_nodes = split_nodes_delimiter([old_node], "`", TextType.CODE)
        self.assertEqual(new_nodes[0].text, "This is a ")
        self.assertEqual(new_nodes[0].text_type.value, "text")
        self.assertEqual(new_nodes[1].text, "code")
        self.assertEqual(new_nodes[1].text_type.value, "code")
        self.assertEqual(new_nodes[2].text, " node")
        self.assertEqual(new_nodes[2].text_type.value, "text")

    def test_invalid_syntax(self):
        old_node = TextNode("This is an `invalid node", TextType.TEXT)
        self.assertRaises(Exception,split_nodes_delimiter,old_node, "`", TextType.CODE)
    
    def test_multiple_split(self):
        old_node = TextNode("This is a **bold** `code` node", TextType.TEXT)
        new_old_nodes = split_nodes_delimiter([old_node], "`", TextType.CODE)
        new_nodes = split_nodes_delimiter(new_old_nodes, "**", TextType.BOLD)
        self.assertEqual(new_nodes[0].text, "This is a ")
        self.assertEqual(new_nodes[0].text_type.value, "text")
        self.assertEqual(new_nodes[1].text, "bold")
        self.assertEqual(new_nodes[1].text_type.value, "bold")
        self.assertEqual(new_nodes[2].text, " ")
        self.assertEqual(new_nodes[2].text_type.value, "text")
        self.assertEqual(new_nodes[3].text, "code")
        self.assertEqual(new_nodes[3].text_type.value, "code")
        self.assertEqual(new_nodes[4].text, " node")
        self.assertEqual(new_nodes[4].text_type.value, "text")

class TestImageLinkExtraction(unittest.TestCase):
    def test_extract_markdown_image(self):
        matches = extract_markdown_images("This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)")
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_markdown_images(self):
        matches = extract_markdown_images("This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)")
        self.assertListEqual([("rick roll", "https://i.imgur.com/aKaOqIh.gif"),("obi wan","https://i.imgur.com/fJRm4Vk.jpeg")], matches)

    def test_extract_incorrect_image(self):
        matches = extract_markdown_images("This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)")
        self.assertListEqual([], matches)

    def test_extract_markdown_link(self):
        matches = extract_markdown_links("This is text with a link [to boot dev](https://www.boot.dev)")
        self.assertListEqual([("to boot dev", "https://www.boot.dev")], matches)

    def test_extract_markdown_links(self):
        matches = extract_markdown_links("This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)")
        self.assertListEqual([("to boot dev", "https://www.boot.dev"), ("to youtube", "https://www.youtube.com/@bootdotdev")], matches)

    def test_extract_incorrect_links(self):
        matches = extract_markdown_links("This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)")
        self.assertListEqual([], matches)

class TestImageDelimiter(unittest.TestCase):
    def test_multiple_images(self):
        old_node = TextNode("This is text with an ![image1](url1) and another ![image2](url2) with a trailing text.", TextType.TEXT)
        new_nodes = split_nodes_image([old_node])
        self.assertEqual(new_nodes[0].text, "This is text with an ")
        self.assertEqual(new_nodes[0].text_type.value, "text")
        self.assertEqual(new_nodes[1].text, "image1")
        self.assertEqual(new_nodes[1].text_type.value, "image")
        self.assertEqual(new_nodes[1].url, "url1")
        self.assertEqual(new_nodes[2].text, " and another ")
        self.assertEqual(new_nodes[2].text_type.value, "text")
        self.assertEqual(new_nodes[3].text, "image2")
        self.assertEqual(new_nodes[3].text_type.value, "image")
        self.assertEqual(new_nodes[3].url, "url2")
        self.assertEqual(new_nodes[4].text, " with a trailing text.")
        self.assertEqual(new_nodes[4].text_type.value, "text")

    def test_single_trailing_text(self):
        old_node = TextNode("![image2](url2) with a trailing text.", TextType.TEXT)
        new_nodes = split_nodes_image([old_node])
        self.assertEqual(new_nodes[0].text, "image2")
        self.assertEqual(new_nodes[0].text_type.value, "image")
        self.assertEqual(new_nodes[0].url, "url2")
        self.assertEqual(new_nodes[1].text, " with a trailing text.")
        self.assertEqual(new_nodes[1].text_type.value, "text")

    def test_no_trailing_text(self):
        old_node = TextNode("This is text with an ![image1](url1)", TextType.TEXT)
        new_nodes = split_nodes_image([old_node])
        self.assertEqual(new_nodes[0].text, "This is text with an ")
        self.assertEqual(new_nodes[0].text_type.value, "text")
        self.assertEqual(new_nodes[1].text, "image1")
        self.assertEqual(new_nodes[1].text_type.value, "image")
        self.assertEqual(new_nodes[1].url, "url1")

    def test_link_image_mix(self):
        old_node = TextNode("This is text with an ![image1](url1) and a link [to boot dev](https://www.boot.dev)", TextType.TEXT)
        new_nodes = split_nodes_image([old_node])
        self.assertEqual(new_nodes[0].text, "This is text with an ")
        self.assertEqual(new_nodes[0].text_type.value, "text")
        self.assertEqual(new_nodes[1].text, "image1")
        self.assertEqual(new_nodes[1].text_type.value, "image")
        self.assertEqual(new_nodes[1].url, "url1")
        self.assertEqual(new_nodes[2].text, " and a link [to boot dev](https://www.boot.dev)")
        self.assertEqual(new_nodes[2].text_type.value, "text")

class TestLinkDelimiter(unittest.TestCase):
    def test_multiple_links(self):
        old_node = TextNode("This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev) with a trailing text.", TextType.TEXT)
        new_nodes = split_nodes_link([old_node])
        self.assertEqual(new_nodes[0].text, "This is text with a link ")
        self.assertEqual(new_nodes[0].text_type.value, "text")
        self.assertEqual(new_nodes[1].text, "to boot dev")
        self.assertEqual(new_nodes[1].text_type.value, "link")
        self.assertEqual(new_nodes[1].url, "https://www.boot.dev")
        self.assertEqual(new_nodes[2].text, " and ")
        self.assertEqual(new_nodes[2].text_type.value, "text")
        self.assertEqual(new_nodes[3].text, "to youtube")
        self.assertEqual(new_nodes[3].text_type.value, "link")
        self.assertEqual(new_nodes[3].url, "https://www.youtube.com/@bootdotdev")
        self.assertEqual(new_nodes[4].text, " with a trailing text.")
        self.assertEqual(new_nodes[4].text_type.value, "text")

    def test_single_trailing_text(self):
        old_node = TextNode("[to youtube](https://www.youtube.com/@bootdotdev) with a trailing text.", TextType.TEXT)
        new_nodes = split_nodes_link([old_node])
        self.assertEqual(new_nodes[0].text, "to youtube")
        self.assertEqual(new_nodes[0].text_type.value, "link")
        self.assertEqual(new_nodes[0].url, "https://www.youtube.com/@bootdotdev")
        self.assertEqual(new_nodes[1].text, " with a trailing text.")
        self.assertEqual(new_nodes[1].text_type.value, "text")

    def test_no_trailing_text(self):
        old_node = TextNode("This is text with a link [to boot dev](https://www.boot.dev)", TextType.TEXT)
        new_nodes = split_nodes_link([old_node])
        self.assertEqual(new_nodes[0].text, "This is text with a link ")
        self.assertEqual(new_nodes[0].text_type.value, "text")
        self.assertEqual(new_nodes[1].text, "to boot dev")
        self.assertEqual(new_nodes[1].text_type.value, "link")
        self.assertEqual(new_nodes[1].url, "https://www.boot.dev")

    def test_link_image_mix(self):
        old_node = TextNode("This is text with an ![image1](url1) and a link [to boot dev](https://www.boot.dev)", TextType.TEXT)
        new_nodes = split_nodes_link([old_node])
        self.assertEqual(new_nodes[0].text, "This is text with an ![image1](url1) and a link ")
        self.assertEqual(new_nodes[0].text_type.value, "text")
        self.assertEqual(new_nodes[1].text, "to boot dev")
        self.assertEqual(new_nodes[1].text_type.value, "link")
        self.assertEqual(new_nodes[1].url, "https://www.boot.dev")

class TestTextToTextNodes(unittest.TestCase):
    def test_all_types(self):
        text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        nodes = text_to_textnodes(text)
        self.assertListEqual(
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("text", TextType.BOLD),
                TextNode(" with an ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word and a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" and an ", TextType.TEXT),
                TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
                TextNode(" and a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://boot.dev"),
            ],
            nodes,
        )

if __name__ == "__main__":
    unittest.main()