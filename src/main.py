from textnode import TextNode, TextType
from htmlnode import HTMLNode, LeafNode, ParentNode

def main():
        node = ParentNode(
            "a",
            [
                ParentNode("x",
                            [
                                LeafNode("b", "Bold text"),
                                LeafNode(None, "Normal text")
                            ]
                ),
                LeafNode("i", "italic text"),            ],
            {
                "href": "https://google.com",
                "target": "_blank"
            }
        )

        print(f"Node 1 to HTML: \n {node.to_html()}")

main()