from htmlnode import *
from textnode import *
from extract_markdown import *

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

def split_nodes_image(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        #finds all image nodes within node
        extracted_images = extract_markdown_images(node.text)
        #checks if there are any image links and adds plain text node back to list if not
        if len(extracted_images) < 1:
            #check if node text is empty, and skip if so
            if node.text != None and node.text != "":
                new_nodes.append(node)
            continue
        # separates a node into individual components (text sections and image sections)
        node_sections = [node.text]
        final_node_sections = []
        for image in extracted_images:
            node_sections = node_sections[len(node_sections)-1].split(f"![{image[0]}]({image[1]})", 1)
            final_node_sections.extend([node_sections[0], f"![{image[0]}]({image[1]})"])
        if len(node_sections[1]) > 0:
            final_node_sections.append(node_sections[1])

        #populate list with all proper node attributes for each section
        new_node = []
        i = 0
        for section in final_node_sections:
            if "![" in section:
                next_node = TextNode(extracted_images[i][0], TextType.IMAGE, extracted_images[i][1])
                i += 1
            elif section == "":
                continue
            else:
                next_node = TextNode(section, TextType.TEXT)
            new_nodes.append(next_node)
    return new_nodes
                
def split_nodes_link(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        #finds all link nodes within node
        extracted_links = extract_markdown_links(node.text)
        #checks if there are any image links and adds plain text node back to list if not
        if len(extracted_links) < 1:
            #check if node text is empty, and skip if so
            if node.text != None and node.text != "":
                new_nodes.append(node)
            continue
        # separates a node into individual components (text sections and link sections)
        node_sections = [node.text]
        final_node_sections = []
        for link in extracted_links:
            node_sections = node_sections[len(node_sections)-1].split(f"[{link[0]}]({link[1]})", 1)
            final_node_sections.extend([node_sections[0], f"[{link[0]}]({link[1]})"])
        if len(node_sections[1]) > 0:
            final_node_sections.append(node_sections[1])

        #populate list with all proper node attributes for each section
        new_node = []
        i = 0
        for section in final_node_sections:
            if "](" in section and "![" not in section:
                next_node = TextNode(extracted_links[i][0], TextType.LINK, extracted_links[i][1])
                i += 1
            elif section == "":
                continue
            else:
                next_node = TextNode(section, TextType.TEXT)
            new_nodes.append(next_node)
    return new_nodes

def text_to_textnodes(text):
    text_as_node = [TextNode(text, TextType.TEXT)]
    code = split_nodes_delimiter(text_as_node, "`", TextType.CODE)
    bold = split_nodes_delimiter(code, "**", TextType.BOLD)
    italics = split_nodes_delimiter(bold, "*", TextType.ITALIC)
    images = split_nodes_image(italics)
    italics_underscore = split_nodes_delimiter(images, "_", TextType.ITALIC)
    links = split_nodes_link(italics_underscore)
    return links   
