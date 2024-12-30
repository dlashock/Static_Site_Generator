from textnode import TextType, TextNode

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    node_list = []
    for node in old_nodes:
        split_text = node.text.split(delimiter)
        if len(split_text) %2 == 0:
            raise Exception(f"Invalid Markdown Syntax. Missing delimiter: {delimiter}")
        for index, text in enumerate(split_text):
            if index % 2 == 0:
                node_list.append(TextNode(text, TextType.TEXT))
            else:
                node_list.append(TextNode(text, text_type))
    return node_list