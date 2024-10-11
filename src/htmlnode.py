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
    