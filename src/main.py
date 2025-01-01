import re
from textnode import TextNode, TextType
from htmlnode import HTMLNode, LeafNode, ParentNode
from inline_markdown import (
    split_nodes_delimiter, 
    extract_markdown_images, 
    extract_markdown_links,
    split_nodes_image,
    split_nodes_link,
    text_to_textnodes
)
from block_markdown import (
    markdown_to_blocks,
    is_heading, 
    block_to_block_type, 
    is_code, 
    is_quote, 
    is_unordered_list,
    is_ordered_list
)

def main():
    pass

    ordered_list = "1. Test\n2. Test 2\n3. Line 3\n4. Line 4"
    unordered_list = "* Line 1\n* Line 2\n- Line 3 with different bullet\n- Line 4"
    quote = ">This is a quote\n>There are many like it\n>But this one is mine"
    code = "```This is my awesome code block\nIt looks super good and I'm very happy to have it```"
    heading = "### This is a header"
    
    print(f"Heading: {block_to_block_type(heading)}")
    print(f"Code: {block_to_block_type(code)}")
    print(f"Quote: {block_to_block_type(quote)}")
    print(f"Unordered List: {block_to_block_type(unordered_list)}")
    print(f"Ordered List: {block_to_block_type(ordered_list)}")

main()