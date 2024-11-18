from htmlnode import *
from textnode import *

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for node in old_nodes:
        if node.text_type == TextType.TEXT:
            
            if node.text.count(delimiter) % 2 != 0:
                raise ValueError("Mismatched set of delimiters, invalid syntax")

            split_up = node.text.split(delimiter)
            new_node = []

            for part in split_up:
                if part == "":
                    continue
                if split_up.index(part) == 0 or split_up.index(part) % 2 == 0:
                    new_node.append(TextNode(part, TextType.TEXT))
                else:
                    new_node.append(TextNode(part, text_type))
            
            new_nodes.extend(new_node)
        
        else:
            new_nodes.append(node)
    
    return new_nodes