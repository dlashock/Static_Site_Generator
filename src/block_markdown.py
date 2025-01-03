import re
from htmlnode import ParentNode
from inline_markdown import text_to_textnodes
from textnode import text_node_to_html_node


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
    body = ParentNode("div", [], None)
    for block in blocks:
        block_type = block_to_block_type(block)
        match block_type:
            case "paragraph":
                node = create_paragraph_node(block)
            case "heading":
                node = parse_header_block(block)
            case "code":
                node = create_code_node(block)
            case "quote":
                node = create_quote_node(block)
            case "unordered_list":
                node = ulist_to_html_nodes(block)
            case "ordered_list":
                node = olist_to_html_nodes(block)
            case _:
                raise Exception("Invalid block type detected")
        body.children.append(node)
    return body
            
def text_to_children(block):
    children = text_to_textnodes(block)
    html_children = []
    for child in children:
        child = text_node_to_html_node(child)
        html_children.append(child)
    return html_children

def create_paragraph_node(block):
    lines = block.split("\n")
    paragraph = " ".join(lines)
    children = text_to_children(paragraph)
    return ParentNode("p", children)

def ulist_to_html_nodes(block):
    parent_node = ParentNode("ul", [])
    list_items = block.split("\n")
    for item in list_items:
        children = text_to_children(item[2:])
        li_node = ParentNode("li", children)
        parent_node.children.append(li_node)
    return parent_node

def olist_to_html_nodes(block):
    parent_node = ParentNode("ol", [])
    list_items = block.split("\n")
    for item in list_items:
        text = re.sub(r"^\d+\.\s", "", item)
        children = text_to_children(text)
        li_node = ParentNode("li", children)
        parent_node.children.append(li_node)
    return parent_node

def parse_header_block(block):
    match = re.match(r"^(#{1,6})\s(?![#])", block)
    if match:
        level = len(match.group(1))
        children = text_to_children(block[level+1:])
        return ParentNode(f"h{level}", children, None)
    else:
        raise ValueError("Invalid header block")
    
def create_code_node(block):
    if not block.startswith("```") or block.endswith("```"):
        raise ValueError("Invalid code block")
    text = block[4:-3]
    children = text_to_children(text)
    inner_node = ParentNode("code", children)
    outer_node = ParentNode("pre", [inner_node])
    return outer_node

def create_quote_node(block):
    lines = block.split("\n")
    new_lines = []
    for line in lines:
        if not line.startswith(">"):
            raise ValueError("Invalid quote block")
        new_lines.append(line.lstrip(">").strip())
    quote = " ".join(new_lines)
    children = text_to_children(quote)
    return ParentNode("blockquote", children)