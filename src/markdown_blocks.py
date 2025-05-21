from enum import Enum
import re

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
    