from textnode import *
from htmlnode import *

def main():
    sample_node = TextNode("sample text", text_type_italic, "www.sample.com")
    print(sample_node)

    sample_html = HTMLNode("tag", "value", ["child"], {"attribute":"attribute_body"})
    print(sample_html)

main()
