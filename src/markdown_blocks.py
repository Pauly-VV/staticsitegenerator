from enum import Enum
import re
from htmlnode import *
from split_nodes_delimiter import *

class BlockType(Enum):
    paragraph = "paragraph"
    heading = "heading"
    code = "code"
    quote = "quote"
    unordered_list = "unordered_list"
    ordered_list = "ordered_list"

def markdown_to_blocks(markdown):
    split_text = markdown.strip().split("\n\n")
    i = 0
    for block in split_text:
        split_text[i] = block.strip()
        i += 1
    while "" in split_text:
        split_text.remove("")
        
    return split_text

def block_to_block_type(markdown_block):
    if re.match(r"#{1,6} .+", markdown_block) != None:
        return BlockType.heading
    elif markdown_block[0:3] == "```" and markdown_block[-3:] == "```":
        return BlockType.code
    
    lines = markdown_block.split("\n")
    i = 0
    for line in lines:
        lines[i] = line.strip()
        i += 1

    j = 1
    for line in lines:
        if line[0] == ">" or line[0:2] == "- " or line[0:3] == f"{j}. ":
            j += 1
        else:
            return BlockType.paragraph
        
    if markdown_block[0] == ">":
        return BlockType.quote
    elif markdown_block[0] == "-":
        return BlockType.unordered_list
    elif markdown_block[0] == "1":
        return BlockType.ordered_list

def block_type_to_tag(block):
    if block_to_block_type(block) == BlockType.heading:
        i = 0
        for letter in block:
            if letter == "#":
                i += 1
            else:
                break
        return f"h{i}"


def unordered_block_to_html_nodes(unordered_list_block):
    list_children = []
    list_items = unordered_list_block.split("\n")
    i = 0
    for i in range(len(list_items)):
        #strip the hyphen
        list_items[i] = list_items[i].lstrip("- ")

        #convert text of point into necessary text nodes
        text_children = text_to_textnodes(list_items[i])

        #convert each text node to html node
        text_children_html = []
        for node in text_children:
            text_children_html.append(text_node_to_html_node(node))

        #add a list element with the text broken into nodes as children
        list_children.append(ParentNode("li", text_children_html))
    
    #return full list, with children being each point
    return ParentNode("ul", list_children)
    
def ordered_block_to_html_nodes(ordered_list_block):
    list_children = []
    list_items = ordered_list_block.split("\n")
    i = 0
    for i in range(len(list_items)):
        #strip the number and dot
        list_items[i] = list_items[i].lstrip("1234567890. ")

        #convert text of point into necessary text nodes
        text_children = text_to_textnodes(list_items[i])

        #convert each text node to html node
        text_children_html = []
        for node in text_children:
            text_children_html.append(text_node_to_html_node(node))

        #add a list element with the text broken into nodes as children
        list_children.append(ParentNode("li", text_children_html))
    
    #return full list, with children being each point
    return ParentNode("ol", list_children)

def quote_block_to_html_nodes(quote_block):
    quote_lines = quote_block.split("\n")
    i = 0
    for i in range(len(quote_lines)):
        #strip the >
        quote_lines[i] = quote_lines[i].lstrip("> ")

    #push back together
    text = " ".join(quote_lines)
    
    #return full list, with children being all text as html nodes
    return ParentNode("blockquote", text_to_children(text))

def heading_block_to_html_nodes(heading_block):
    match_group = re.match(r"(#{1,6}) (.*)", heading_block)
    text = match_group.group(2)
    num_hashes = len(match_group.group(1))
    return ParentNode(f"h{num_hashes}", text_to_children(text))

def paragraph_block_to_html_nodes(paragraph_block):
    text = " ".join(paragraph_block.split("\n"))
    return ParentNode("p", text_to_children(text))

def text_to_children(text):
    text_nodes = text_to_textnodes(text)
    children = []
    for node in text_nodes:
        children.append(text_node_to_html_node(node))
    return children

def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    list_of_blocks_as_html = []
    for block in blocks:
        #check block type
        block_type = block_to_block_type(block)

        #deal with unordered lists
        if block_type == BlockType.unordered_list:
            block_as_html = unordered_block_to_html_nodes(block)
        
        #deal with ordered lists
        elif block_type == BlockType.ordered_list:
            block_as_html = ordered_block_to_html_nodes(block)
        
        #deal with paragraph
        elif block_type == BlockType.paragraph:
            block_as_html = paragraph_block_to_html_nodes(block)

        #deal with heading
        elif block_type == BlockType.heading:
            block_as_html = heading_block_to_html_nodes(block)

        #deal with code
        elif block_type == BlockType.code:
            text_list = block.split("\n")
            shortened = text_list[1:-1]
            text = "\n".join(shortened) + "\n"
            block_as_html = ParentNode("pre", [ParentNode("code", [text_node_to_html_node(TextNode(text, TextType.TEXT))])])

        #deal with quote
        elif block_type == BlockType.quote:
            block_as_html = quote_block_to_html_nodes(block)
        
        #append result to full list
        list_of_blocks_as_html.append(block_as_html)
    
    #combine list of blocks as html into one string of html
    full_html_node = ParentNode("div", list_of_blocks_as_html)
    return full_html_node