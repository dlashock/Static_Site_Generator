import re
from textnode import TextType, TextNode

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    node_list = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            node_list.append(node)
        else:
            split_text = node.text.split(delimiter)
            if len(split_text) %2 == 0 and len(split_text) > 1:
                raise Exception(f"Invalid Markdown Syntax. Missing delimiter: {delimiter}")
            for index, text in enumerate(split_text):
                if split_text[index] == "":
                    continue
                elif index % 2 == 0:
                    node_list.append(TextNode(text, TextType.TEXT))
                else:
                    node_list.append(TextNode(text, text_type))
    return node_list

    '''----------------------------------------------------------------
    ---       Markdown Functions from Boot.Dev Solution
    ----------------------------------------------------------------'''

def extract_markdown_images(text):
    pattern = r"!\[([^\[\]]*)\]\(([^\(\)]*)\)"
    matches = re.findall(pattern, text)
    return matches


def extract_markdown_links(text):
    pattern = r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)"
    matches = re.findall(pattern, text)
    return matches

    '''----------------------------------------------------------------
    ---         Markdown Functions written by me
    ----------------------------------------------------------------'''

# def extract_markdown_images(text):
#     alt_matches = re.findall(r"!\[([^\[\]]*)\]", text)
#     image_matches = re.findall(r"\w+.\/\/[-A-Za-z0-9@:%_\+.~#?&//=]{2,256}", text)
#     return list(zip(alt_matches, image_matches))

# def extract_markdown_links(text):
#     anchor_matches = re.findall(r"(?<!!)\[([^\[\]]*)\]", text)
#     link_matches = re.findall(r"\(([^\(\)]*)\)", text)
#     return list(zip(anchor_matches, link_matches))

def split_nodes_image(old_nodes):
    node_list = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            node_list.append(node)
            continue
        if node.text == "":
            continue
        original_text = node.text
        images = extract_markdown_images(original_text)
        if len(images) == 0:
            node_list.append(node)
            continue
        for alt, link in images:
            sections = original_text.split(f"![{alt}]({link})", 1)
            if len(sections) != 2:
                raise ValueError("Invalid markdown, image section not closed")
            if sections[0] != "":
                node_list.append(TextNode(sections[0], TextType.TEXT))
            node_list.append(TextNode(alt, TextType.IMAGE, link))
            original_text = sections[1]
        if original_text != "":
            node_list.append(TextNode(original_text, TextType.TEXT))
    return node_list     

def split_nodes_link(old_nodes):
    node_list = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            node_list.append(node)
            continue
        if node.text == "":
            continue
        original_text = node.text
        links = extract_markdown_links(original_text)
        if len(links) == 0:
            node_list.append(node)
            continue
        for anchor, link in links:
            sections = original_text.split(f"[{anchor}]({link})", 1)
            if len(sections) != 2:
                raise ValueError("Invalid markdown, link section not closed")
            if sections[0] != "":
                node_list.append(TextNode(sections[0], TextType.TEXT))
            node_list.append(TextNode(anchor, TextType.LINK, link))
            original_text = sections[1]
        if original_text != "":
            node_list.append(TextNode(original_text, TextType.TEXT))
    return node_list

def text_to_textnodes(text):
    node = TextNode(text, TextType.TEXT)
    split_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
    split_nodes = split_nodes_delimiter(split_nodes, "*", TextType.ITALIC)
    split_nodes = split_nodes_delimiter(split_nodes, "`", TextType.CODE)
    split_nodes = split_nodes_image(split_nodes)
    split_nodes = split_nodes_link(split_nodes)
    return split_nodes