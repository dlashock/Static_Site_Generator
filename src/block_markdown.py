import re
from htmlnode import HTMLNode, LeafNode, ParentNode
from inline_markdown import text_to_textnodes, TextNode, TextType


def markdown_to_blocks(markdown):
    split_text = markdown.split("\n\n")
    blocks = []
    for item in split_text:
        if item == "":
            continue
        item = item.strip()
        blocks.append(item)
    
    return blocks
        
def block_to_block_type(block):
    if is_heading(block):
        return "heading"
    if is_code(block):
        return "code"
    if is_quote(block):
        return "quote"
    if is_unordered_list(block):
        return "unordered_list"
    if is_ordered_list(block):
        return "ordered_list"
    return "paragraph"
    
def is_heading(text):
    valid = bool(re.match(r"^#{1,6} (?![#])", text))
    return valid

def is_code(text):
    valid = bool(re.match(r"^```[\s\S]*```$", text))
    return valid

def is_quote(text):
    valid = bool(re.match(r"^>.*?", text))
    if not valid:
        return False
    split_text = text.split("\n")
    for line in split_text:
        valid = bool(re.match(r"^>.*?", line))
        if not valid:
            raise Exception("Quote block not formatted correctly")
    return valid

def is_unordered_list(text):
    valid = bool(re.match(r"^[*-]\s", text))
    if not valid:
        return False
    split_text = text.split("\n")
    for line in split_text:
        valid = bool(re.match(r"^[*-]\s", line))
        if not valid:
            raise Exception("Unordered list block not formatted correctly")
    return valid

def is_ordered_list(text):
    valid = bool(re.match(r"^\d+\. .*", text))
    if not valid:
        return False
    split_text = text.split("\n")
    current_list_pos = 1
    for line in split_text:
        valid = bool(re.match(r"^\d+\. .*", line))
        if not valid or current_list_pos != int(line[0]):
            raise Exception("Ordered list block not formatted correctly")
        if current_list_pos < len(split_text):
            current_list_pos += 1
    return valid

def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    for block in blocks:
        block_type = block_to_block_type(block)
        match block_type:
            case "paragraph":
                node = HTMLNode("<p>", block, None, None)
            case "heading":
                if bool(re.match(r"^#{1} (?![#])", block)):
                    node = HTMLNode("<h1>", block, None, None)
                elif bool(re.match(r"^#{2} (?![#])", block)):
                    node = HTMLNode("<h2>", block, None, None)
                elif bool(re.match(r"^#{3} (?![#])", block)):
                    node = HTMLNode("<h3>", block, None, None)
                elif bool(re.match(r"^#{4} (?![#])", block)):
                    node = HTMLNode("<h4>", block, None, None)
                elif bool(re.match(r"^#{5} (?![#])", block)):
                    node = HTMLNode("<h5>", block, None, None)
                elif bool(re.match(r"^#{6} (?![#])", block)):
                    node = HTMLNode("<h6>", block, None, None)
                else:
                    raise Exception("Heading node not properly formatted")
            case "code":
                node = HTMLNode("<code>", block, None, None)
            case "quote":
                node = HTMLNode("<blockquote>", block, None, None)
            case "unordered_list":
                node = HTMLNode("<ul>", None, None)
            case "ordered_list":
                node = HTMLNode("<ol>", block, None, None)
            case _:
                raise Exception("Invalid block type detected")