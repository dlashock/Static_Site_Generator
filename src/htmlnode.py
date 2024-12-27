class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def __repr__(self):
        return f'HTMLNode(Tag:{self.tag}, Value:{self.value}, Children:{self.children}, Props:{self.props})'
                
    def to_html(self):
        raise NotImplementedError("to_html method not implemented")
    
    def props_to_html(self):
        result = ""

        if self.props != None:
            for key, value in self.props.items():
                result += f' {key}="{value}"'
        
        return result
    
class LeafNode(HTMLNode):
    def __init__(self, tag, value, children=None, props=None):
        if children != None:
            raise ValueError("LeafNode cannot have children")
        super().__init__(tag, value, None, props)

    def __repr__(self):
        return f"LeafNode({self.tag}, {self.value}, {self.props})"
    
    def to_html(self):
        if self.value == None:
            raise ValueError("All leaf node must have a value")
        if self.tag == None:
            return self.value
        if self.props == None:
            return f"<{self.tag}>{self.value}</{self.tag}>"

        props_string = ""
        for key, value in self.props.items():
            props_string += f' {key}="{value}"'

        return f"<{self.tag}{props_string}>{self.value}</{self.tag}>"
    
class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, children, props)

    def __repr__(self):
        return f'ParentNode(Tag:{self.tag}, Children:{self.children}, Props:{self.props})'
    
    def to_html(self):
        if self.tag == None:
            raise ValueError("Parent Nodes must have tags")
        if self.children == None:
            raise ValueError("Parent nodes must have children")
        if self.props == None:
            props_string = ""
            for child in self.children:
                props_string += child.to_html()
            
            return f"<{self.tag}>{props_string}</{self.tag}>"
        
