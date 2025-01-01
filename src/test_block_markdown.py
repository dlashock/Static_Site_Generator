import unittest

from block_markdown import markdown_to_blocks, block_to_block_type

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