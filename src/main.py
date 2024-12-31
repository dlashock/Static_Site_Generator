from textnode import TextNode, TextType
from htmlnode import HTMLNode, LeafNode, ParentNode
from inline_markdown import (
    split_nodes_delimiter, 
    extract_markdown_images, 
    extract_markdown_links,
    split_nodes_image,
    split_nodes_link,
)

def main():
    pass

    text = "![image](https://www.example.COM/IMAGE.PNG)"

    link_node = TextNode(
        text,
        TextType.TEXT,
    )
    link_nodes = split_nodes_image([link_node])

    print(link_nodes)

    print(extract_markdown_images(text))

main()