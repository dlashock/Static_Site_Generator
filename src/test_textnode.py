import unittest

from textnode import TextNode, TextType, text_node_to_html_node


class TestTextNode(unittest.TestCase):
    def test_eq(self): #Testing for exact equality
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_eq_with_url(self): #Testing for exact equality with URL
        node = TextNode("This is a text node", TextType.BOLD, "https://google.com")
        node2 = TextNode("This is a text node", TextType.BOLD, "https://google.com")
        self.assertEqual(node, node2)

    def test_eq_with_space(self): #Testing for equality with extra space
        node = TextNode("This is a text node", TextType.BOLD, "https://google.com")
        node2 = TextNode("This is a text node ", TextType.BOLD, "https://google.com")
        self.assertNotEqual(node, node2)

    def test_eq_diff_type(self): #Testing for equality with differing TextType
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.CODE)
        self.assertNotEqual(node, node2)

    def test_eq_one_URL(self): #Testing single defined URL
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD, "https://boot.dev")
        self.assertNotEqual(node, node2)

    def test_eq_none_url(self): #One URL is set to None
        node = TextNode("This is a text node", TextType.BOLD, None)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_not_equal_url(self): #Different name, testing url difference
        node1 = TextNode("This is a text node", TextType.BOLD, "test.com")
        node2 = TextNode("This is a text node", TextType.BOLD, "test2.com")
        self.assertNotEqual(node1, node2)

    def test_equal_different_object(self): #Testing equality against a different type of object
        node1 = TextNode("This is a text node", TextType.BOLD, "test.com")
        node2 = "This is a string"
        self.assertNotEqual(node1, node2)

    def test_equal_different_object_reversed(self): #Testing equality against a different type of object reversed
        node1 = TextNode("This is a text node", TextType.BOLD, "test.com")
        node2 = "This is a string"
        self.assertNotEqual(node2, node1)

    '''
    ---------------------------------------------------------------------
                    TestNode to HTML Testing
    ---------------------------------------------------------------------
    '''
class TestTextNodeToHTMLNode(unittest.TestCase):
    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_image(self):
        node = TextNode("This is an image", TextType.IMAGE, "https://www.boot.dev")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, "")
        self.assertEqual(
            html_node.props,
            {"src": "https://www.boot.dev", "alt": "This is an image"},
        )

    def test_bold(self):
        node = TextNode("This is bold", TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "This is bold")

if __name__ == "__main__":
    unittest.main()