class HTMLNode():
    def __init__(self, tag = None, value = None, children = None, props = None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError
    
    def __eq__(self, other_HTMLNode):
        return (
            self.tag == other_HTMLNode.tag
            and self.value == other_HTMLNode.value
            and self.children == other_HTMLNode.children
            and self.props == other_HTMLNode.props
        )
    
    def props_to_html(self):
        conversion_text = ""
        if self.props != None:
            for item in self.props:
                conversion_text += f' {item}="{self.props[item]}"'
        return conversion_text
    
    def list_to_doublequotes(self):
        output_string = '["' + '", "'.join(self.children) + '"]'
        return output_string
    
    def __repr__(self):
        props_att = self.props_to_html()
        children_list = self.list_to_doublequotes()
        return f'HTMLNode:\ntag = {self.tag} \nvalue = {self.value} \nchildren = {children_list} \nprops = {props_att}'
    

class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, None, props)
        
    def to_html(self):
        if self.value == None:
            raise ValueError("Leaf node requires a value for 'value'")
        if self.tag == None:
            return self.value
        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"

    def __eq__(self, other_LeafNode):
        return (
            self.tag == other_LeafNode.tag
            and self.value == other_LeafNode.value
            and self.props == other_LeafNode.props
        )
    
    def __repr__(self):
        props_att = self.props_to_html()
        return f'HTMLNode:\ntag = {self.tag} \nvalue = {self.value} \nprops = {props_att}'
    
class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, children, props)

    def to_html(self):
        if self.tag == None:
            raise ValueError("Parent node requires a value for 'tag'")
        if self.children == None:
            raise ValueError("Parent node requires a value for 'children'")
        
        children_str = ""
        for x in range(len(self.children)):
            children_str += self.children[x].to_html()

        return f'<{self.tag}{self.props_to_html()}>{children_str}</{self.tag}>'
    
    def __repr__(self):
        props_att = self.props_to_html()
        return f'ParentNode:\ntag = {self.tag} \nchildren = {self.children} \nprops = {props_att}'
