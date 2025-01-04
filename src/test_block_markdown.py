import unittest

from block_markdown import markdown_to_blocks, block_to_block_type, markdown_to_html_node, extract_title

class TestBlockMarkdown(unittest.TestCase):
    def test_markdown_to_blocks(self):
        text = "     # This is a heading\n\n        This is a paragraph of text. It has some **bold** and *italic* words inside of it.\n\n* This is the first list item in a list block\n* This is a list item\n* This is another list item\n"
        blocks = markdown_to_blocks(text)
        expected_result = [
            "# This is a heading",
            "This is a paragraph of text. It has some **bold** and *italic* words inside of it.",
            "* This is the first list item in a list block\n* This is a list item\n* This is another list item",
        ]
        self.assertEqual(blocks, expected_result)

    def test_multi_lists(self):
        text = "* Here is a random list\n* Here is another item in that list\n\n     # This is a heading\n\n        This is a paragraph of text. It has some **bold** and *italic* words inside of it.\n\n* This is the first list item in a list block\n* This is a list item\n* This is another list item\n"
        blocks = markdown_to_blocks(text)
        expected_result = [
            "* Here is a random list\n* Here is another item in that list",
            "# This is a heading",
            "This is a paragraph of text. It has some **bold** and *italic* words inside of it.",
            "* This is the first list item in a list block\n* This is a list item\n* This is another list item",
        ]
        self.assertEqual(blocks, expected_result)

    def test_block_to_block_type(self):
        ordered_list = "1. Test\n2. Test 2\n3. Line 3\n4. Line 4"
        unordered_list = "* Line 1\n* Line 2\n- Line 3 with different bullet\n- Line 4"
        quote = ">This is a quote\n>There are many like it\n>But this one is mine"
        code = "```This is my awesome code block\nIt looks super good and I'm very happy to have it```"
        heading = "### This is a header"
        paragraph = "This is just a normal text paragraph"
        
        self.assertEqual(block_to_block_type(ordered_list), "ordered_list")
        self.assertEqual(block_to_block_type(unordered_list), "unordered_list")
        self.assertEqual(block_to_block_type(quote), "quote")
        self.assertEqual(block_to_block_type(code), "code")
        self.assertEqual(block_to_block_type(heading), "heading")
        self.assertEqual(block_to_block_type(paragraph), "paragraph")

    def test_block_type_exceptions(self):
        ordered_list = "1. Test\n2. Test 2\nThis is not formatted correctly3. Line 3\n4. Line 4"
        unordered_list = "* Line 1\n* Line 2\n- Line 3 with different bullet\nBreaking format- Line 4"
        quote = ">This is a quote\n>There are many like it\nLine doesn't start with the correct character>But this one is mine"
                
        with self.assertRaisesRegex(Exception, "Ordered list block not formatted correctly"):
            block_to_block_type(ordered_list)
        with self.assertRaisesRegex(Exception, "Unordered list block not formatted correctly"):
            block_to_block_type(unordered_list)
        with self.assertRaisesRegex(Exception, "Quote block not formatted correctly"):
            block_to_block_type(quote)

    def test_extract_h1(self):
        header = "# This is a test header"
        header2 = "## This is an improperly formatted H1 header"
        header3 = "# This is a header with whitespace at the end   "
        header4 = "This is a test line\n# there is a header here\n##Header not here"
        self.assertEqual(extract_title(header), "This is a test header")
        with self.assertRaisesRegex(Exception, "Missing H1 header"):
            extract_title(header2)
        self.assertEqual(extract_title(header3), "This is a header with whitespace at the end")
        self.assertEqual(extract_title(header4), "there is a header here")

class TestMarkdownToHTML(unittest.TestCase):
    def test_paragraph(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p></div>",
        )

    def test_paragraphs(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with *italic* text and `code` here

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_lists(self):
        md = """
- This is a list
- with items
- and *more* items

1. This is an `ordered` list
2. with items
3. and more items

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ul><li>This is a list</li><li>with items</li><li>and <i>more</i> items</li></ul><ol><li>This is an <code>ordered</code> list</li><li>with items</li><li>and more items</li></ol></div>",
        )

    def test_headings(self):
        md = """
# this is an h1

this is paragraph text

## this is an h2
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h1>this is an h1</h1><p>this is paragraph text</p><h2>this is an h2</h2></div>",
        )

    def test_blockquote(self):
        md = """
> This is a
> blockquote block

this is paragraph text

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><blockquote>This is a blockquote block</blockquote><p>this is paragraph text</p></div>",
        )

if __name__ == "__main__":
    unittest.main()