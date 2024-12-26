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