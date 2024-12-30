import unittest

from textnode import TextNode, TextType, text_node_to_html_node
from inline_markdown import split_nodes_delimiter, extract_markdown_images, extract_markdown_links

class TestSplitNode(unittest.TestCase):
    def test_valid_split(self):
        nodes = [TextNode("Hello 'World'", TextType.TEXT)]
        result = split_nodes_delimiter(nodes, "'", TextType.CODE)
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0].text, "Hello ")
        self.assertEqual(result[0].text_type, TextType.TEXT)
        self.assertEqual(result[1].text, "World")
        self.assertEqual(result[1].text_type, TextType.CODE)

    def test_no_split(self):
        nodes = [TextNode("HelloWorld", TextType.TEXT)]
        result = split_nodes_delimiter(nodes, "**", TextType.BOLD)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].text, "HelloWorld")
        self.assertEqual(result[0].text_type, TextType.TEXT)

    def test_non_text_node(self):
        nodes = [TextNode("Hello", TextType.ITALIC)]
        result = split_nodes_delimiter(nodes, "*", TextType.ITALIC)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].text, "Hello")
        self.assertEqual(result[0].text_type, TextType.ITALIC)

    def test_invalid_markdown_syntax(self):
        nodes = [TextNode("Hello **World", TextType.TEXT)]
        with self.assertRaisesRegex(Exception, "Invalid Markdown Syntax. Missing delimiter: \*\*"): #Check the exception message
            split_nodes_delimiter(nodes, "**", TextType.BOLD)

    def test_invalid_markdown_syntax_2(self):
        nodes = [TextNode("Hello *World", TextType.TEXT)]
        with self.assertRaisesRegex(Exception, "Invalid Markdown Syntax. Missing delimiter: *"): #Check the exception message
            split_nodes_delimiter(nodes, "*", TextType.ITALIC)

    def test_invalid_markdown_syntax_3(self):
        nodes = [TextNode("Hello'", TextType.TEXT)]
        with self.assertRaisesRegex(Exception, "Invalid Markdown Syntax. Missing delimiter: '"): #Check the exception message
            split_nodes_delimiter(nodes, "'", TextType.CODE)

    def test_splitnode_bold_and_italic_values(self):
        node = TextNode("This **is** a text node", TextType.TEXT)
        node2 = TextNode("**This** is a text *node*", TextType.TEXT)
        node_list = [node, node2]
        node_list = split_nodes_delimiter(node_list, "**", TextType.BOLD)
        node_list = split_nodes_delimiter(node_list, "*", TextType.ITALIC)
        self.assertEqual(node_list[1].text_type, TextType.BOLD)
        self.assertEqual(node_list[1].text, "is")
        self.assertEqual(node_list[3].text_type, TextType.BOLD)
        self.assertEqual(node_list[3].text, "This")
        self.assertEqual(node_list[5].text_type, TextType.ITALIC)
        self.assertEqual(node_list[5].text, "node")
###--------------------------------------------------------------
###                 Tests from Boot.Dev Solution
###--------------------------------------------------------------
    def test_delim_bold(self):
        node = TextNode("This is text with a **bolded** word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("bolded", TextType.BOLD),
                TextNode(" word", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_delim_bold_double(self):
        node = TextNode(
            "This is text with a **bolded** word and **another**", TextType.TEXT
        )
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("bolded", TextType.BOLD),
                TextNode(" word and ", TextType.TEXT),
                TextNode("another", TextType.BOLD),
            ],
            new_nodes,
        )

    def test_delim_bold_multiword(self):
        node = TextNode(
            "This is text with a **bolded word** and **another**", TextType.TEXT
        )
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("bolded word", TextType.BOLD),
                TextNode(" and ", TextType.TEXT),
                TextNode("another", TextType.BOLD),
            ],
            new_nodes,
        )

    def test_delim_italic(self):
        node = TextNode("This is text with an *italic* word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "*", TextType.ITALIC)
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_delim_bold_and_italic(self):
        node = TextNode("**bold** and *italic*", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        new_nodes = split_nodes_delimiter(new_nodes, "*", TextType.ITALIC)
        self.assertListEqual(
            [
                TextNode("bold", TextType.BOLD),
                TextNode(" and ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
            ],
            new_nodes,
        )

    def test_delim_code(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" word", TextType.TEXT),
            ],
            new_nodes,
        )

class TestMarkdownLinksAndImages(unittest.TestCase):
    def test_multiple_images(self):
        text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        expected_result = [('rick roll', 'https://i.imgur.com/aKaOqIh.gif'), ('obi wan', 'https://i.imgur.com/fJRm4Vk.jpeg')]
        self.assertListEqual(extract_markdown_images(text), expected_result)

    def test_multiple_links(self):
        text = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        expected_result = [("to boot dev", "https://www.boot.dev"), ("to youtube", "https://www.youtube.com/@bootdotdev")]
        self.assertListEqual(extract_markdown_links(text), expected_result)

    def test_image_with_link(self):
        text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) image and link [to youtube](https://www.youtube.com/@bootdotdev)"
        expected_result = [('rick roll', 'https://i.imgur.com/aKaOqIh.gif')]
        self.assertListEqual(extract_markdown_images(text), expected_result)

    def test_image_with_link(self):
        text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) image and link [to youtube](https://www.youtube.com/@bootdotdev)"
        expected_result = [("to youtube", "https://www.youtube.com/@bootdotdev")]
        self.assertListEqual(extract_markdown_links(text), expected_result)

if __name__ == "__main__":
    unittest.main()