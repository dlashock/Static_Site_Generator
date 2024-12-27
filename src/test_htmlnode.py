import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode


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

    '''
    ---------------------------------------------------------------------
                    LeafNode Class Testing
    ---------------------------------------------------------------------
    '''

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
    
    def test_to_html_no_tag(self):
        node = LeafNode(None, "Hello, world!")
        self.assertEqual(node.to_html(), "Hello, world!")

    

    '''
    ---------------------------------------------------------------------
                    ParentNode Class Testing
    ---------------------------------------------------------------------
    '''

    def test_parentnode_to_html(self):
        node = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )
        expected_result = '<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>'
        self.assertEqual(node.to_html(), expected_result)

    def test_nested_parents(self):
        node = ParentNode(
            "a",
            [
                ParentNode("x",
                            [
                                LeafNode("b", "Bold text"),
                                LeafNode(None, "Normal text")
                            ]
                ),
                LeafNode("i", "italic text"),            ],
            {
                "href": "https://google.com",
                "target": "_blank"
            }
        )
        expected_result = '<a href="https://google.com" target="_blank"><x><b>Bold text</b>Normal text</x><i>italic text</i></a>'
        self.assertEqual(node.to_html(), expected_result)

    def test_headings(self):
        node = ParentNode(
            "h2",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )
        self.assertEqual(
            node.to_html(),
            "<h2><b>Bold text</b>Normal text<i>italic text</i>Normal text</h2>",
        )

if __name__ == "__main__":
    unittest.main()