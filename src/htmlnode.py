

class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError
    
    def props_to_html(self):
        ans = ""
        if not self.props:
            return ""
        for k in self.props:
            ans += f" {k}=\"{self.props[k]}\""
        return ans

    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"
    

class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, None, props)

    def to_html(self):
        if not self.value:
            raise ValueError
        if not self.tag:
            return str(self.value)
        else:
            return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"

class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, children, props)

    def to_html(self):
        if not self.tag:
            raise ValueError(f"Error: tried to print a parent node with a missing tag")
        if not self.children:
            raise ValueError("Error: tried to print a parent node with no children")
        
        child_html = ""
        for c in self.children:
            child_html += c.to_html()

        return f"<{self.tag}{self.props_to_html()}>{child_html}</{self.tag}>"