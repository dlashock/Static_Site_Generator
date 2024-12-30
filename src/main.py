from textnode import TextNode, TextType
from htmlnode import HTMLNode, LeafNode, ParentNode
from splitnode import split_nodes_delimiter

def main():
    pass
    node = TextNode("This **is** a text node", TextType.TEXT)
    node2 = TextNode("**This** is a text *node*", TextType.TEXT)
    node_list = [node, node2]
    node_list = split_nodes_delimiter(node_list, "**", TextType.BOLD)
    node_list = split_nodes_delimiter(node_list, "*", TextType.ITALIC)
    for node in node_list:
        print(f"This is a node: {node}")

main()