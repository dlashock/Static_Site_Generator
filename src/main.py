from textnode import TextNode, TextType
from htmlnode import HTMLNode, LeafNode, ParentNode
from inline_markdown import split_nodes_delimiter, extract_markdown_images, extract_markdown_links

def main():
    text3 = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) image and link [to youtube](https://www.youtube.com/@bootdotdev)"
    print(extract_markdown_links(text3))

main()