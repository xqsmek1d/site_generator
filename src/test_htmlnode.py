import unittest
from htmlnode import HTMLNode

class TestHTMLNode(unittest.TestCase):

    def test_no_props(self):
        node = HTMLNode("p", "Lorem Ipsum")
        self.assertEqual(node.props_to_html(),"")

    def test_empty_props(self):
        node = HTMLNode("p", "Lorem Ipsum", None, props={})
        self.assertEqual(node.props_to_html(),"")

    def test_one_prop(self):
        node = HTMLNode("p", "Lorem Ipsum", None, props={"href":"https://www.google.com"})
        self.assertEqual(node.props_to_html(), ' href="https://www.google.com"')

    def test_more_props(self):
        node = HTMLNode("p", "Lorem Ipsum", None, props={"href":"https://www.lipsum.com/", "target": "_blank"})
        self.assertEqual(node.props_to_html(), ' href="https://www.lipsum.com/" target="_blank"')

    def test_full_object(self):
        child = HTMLNode("p", "I am Google's child")
        node = HTMLNode("h1", "Google link", [child], props={"href":"https://www.google.com", "target": "_blank"})
        self.assertEqual(node.tag, "h1")
        self.assertEqual(node.value, "Google link")
        self.assertEqual(node.children, [child])
        self.assertEqual(node.props, {"href":"https://www.google.com", "target": "_blank"})

if __name__ == "__main__":
    unittest.main()