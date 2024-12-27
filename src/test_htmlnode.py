import unittest

from htmlnode import HTMLNode, LeafNode


class TestHTMLNode(unittest.TestCase):
    def test_to_html_props(self):
        node = HTMLNode(
            "div",
            "Hello, world!",
            None,
            {"class": "greeting", "href": "https://boot.dev"},
        )
        self.assertEqual(
            node.props_to_html(),
            ' class="greeting" href="https://boot.dev"',
        )

    def test_values(self):
        node = HTMLNode(
            "div",
            "I wish I could read",
        )
        self.assertEqual(
            node.tag,
            "div",
        )
        self.assertEqual(
            node.value,
            "I wish I could read",
        )
        self.assertEqual(
            node.children,
            None,
        )
        self.assertEqual(
            node.props,
            None,
        )

    def test_repr(self):
        node = HTMLNode(
            "p",
            "What a strange world",
            None,
            {"class": "primary"},
        )
        self.assertEqual(
            node.__repr__(),
            "HTMLNode(Tag:p, Value:What a strange world, Children:None, Props:{'class': 'primary'})",
        )

    def test_leafnode_values(self):
        node = LeafNode(
            "p",
            "What a strange world",
            None,
            {"href": "https://boot.dev"}
        )
        self.assertEqual(
            node.tag,
            "p"
        )
        self.assertEqual(
            node.value,
            "What a strange world",
        )
        self.assertEqual(
            node.props,
            {"href": "https://boot.dev"}
        )

    def test_leafnode_to_html_1(self): #testing a single prop
        node = LeafNode(
            "a",
            "What a strange world",
            None,
            {"href": "https://boot.dev"}
        )
        self.assertEqual(
            node.to_html(),
            '<a href="https://boot.dev">What a strange world</a>',
        )

    def test_leafnode_to_html_2(self): #testing 2 props
        node = LeafNode(
            "a",
            "What a strange world",
            None,
            {"href": "https://boot.dev",
             "target": "_blank"}
        )
        self.assertEqual(
            node.to_html(),
            '<a href="https://boot.dev" target="_blank">What a strange world</a>',
        )

    def test_leafnode_repr(self):
        node = LeafNode(
            "p",
            "What a strange world",
            None,
            {"class": "primary"},
        )
        self.assertEqual(
            node.__repr__(),
            "HTMLNode(Tag:p, Value:What a strange world, Children:None, Props:{'class': 'primary'})",
        )
    
if __name__ == "__main__":
    unittest.main()