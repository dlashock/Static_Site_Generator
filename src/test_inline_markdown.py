import unittest

from textnode import TextNode, TextType, text_node_to_html_node
from inline_markdown import (
    split_nodes_delimiter, 
    extract_markdown_images, 
    extract_markdown_links,
    split_nodes_image,
    split_nodes_link,
    text_to_textnodes
)

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
        with self.assertRaisesRegex(Exception, "Invalid Markdown Syntax. Section not closed"): #Check the exception message
            split_nodes_delimiter(nodes, "**", TextType.BOLD)

    def test_invalid_markdown_syntax_2(self):
        nodes = [TextNode("Hello *World", TextType.TEXT)]
        with self.assertRaisesRegex(Exception, "Invalid Markdown Syntax. Section not closed"): #Check the exception message
            split_nodes_delimiter(nodes, "*", TextType.ITALIC)

    def test_invalid_markdown_syntax_3(self):
        nodes = [TextNode("Hello'", TextType.TEXT)]
        with self.assertRaisesRegex(Exception, "Invalid Markdown Syntax. Section not closed"): #Check the exception message
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

    def test_image_node(self):
        image_node = TextNode(
        "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)",
        TextType.TEXT,
        )
        expected_result = [
            TextNode("This is text with a ", TextType.TEXT, None),
            TextNode("rick roll", TextType.IMAGE, "https://i.imgur.com/aKaOqIh.gif"),
            TextNode(" and ", TextType.TEXT, None),
            TextNode("obi wan", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
        ]
        self.assertEqual(split_nodes_image([image_node]), expected_result)

    def test_link_node(self):
        link_node = TextNode(
        "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)",
        TextType.TEXT,
        )
        expected_result = [
            TextNode("This is text with a link ", TextType.TEXT, None),
            TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
            TextNode(" and ", TextType.TEXT, None),
            TextNode("to youtube", TextType.LINK, "https://www.youtube.com/@bootdotdev"),
        ]
        self.assertEqual(split_nodes_link([link_node]), expected_result)

    def test_link_node_with_image(self):
        node = TextNode(
        "This is text with a link [to boot dev](https://www.boot.dev) and image ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg",
        TextType.TEXT,
        )
        expected_result = [
            TextNode("This is text with a link ", TextType.TEXT, None),
            TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
            TextNode(" and image ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg", TextType.TEXT, None)
        ]
        self.assertEqual(split_nodes_link([node]), expected_result)

    def test_image_node_with_link(self):
        node = TextNode(
        "This is text with a link [to boot dev](https://www.boot.dev) and image ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)",
        TextType.TEXT,
        )
        expected_result = [
            TextNode("This is text with a link [to boot dev](https://www.boot.dev) and image ", TextType.TEXT, None),
            TextNode("obi wan", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
        ]
        self.assertEqual(split_nodes_image([node]), expected_result)

    def test_empty_node(self):
        node = TextNode("", TextType.TEXT)
        self.assertEqual(split_nodes_image([node]), [])
        self.assertEqual(split_nodes_link([node]), [])


    def test_split_image(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
            ],
            new_nodes,
        )

    def test_split_image_single(self):
        node = TextNode(
            "![image](https://www.example.COM/IMAGE.PNG)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("image", TextType.IMAGE, "https://www.example.COM/IMAGE.PNG"),
            ],
            new_nodes,
        )

    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

    def test_split_links(self):
        node = TextNode(
            "This is text with a [link](https://boot.dev) and [another link](https://blog.boot.dev) with text that follows",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://boot.dev"),
                TextNode(" and ", TextType.TEXT),
                TextNode("another link", TextType.LINK, "https://blog.boot.dev"),
                TextNode(" with text that follows", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_all_together(self):
        text = "This is **text** with an *italic* word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        nodes = text_to_textnodes(text)
        expected_result = [
            TextNode("This is ", TextType.TEXT, None),
            TextNode("text", TextType.BOLD, None),
            TextNode(" with an ", TextType.TEXT, None),
            TextNode("italic", TextType.ITALIC, None),
            TextNode(" word and a ", TextType.TEXT, None),
            TextNode("code block", TextType.CODE, None),
            TextNode(" and an ", TextType.TEXT, None),
            TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
            TextNode(" and a ", TextType.TEXT, None),
            TextNode("link", TextType.LINK, "https://boot.dev"),
        ]
        self.assertEqual(nodes, expected_result)


if __name__ == "__main__":
    unittest.main()