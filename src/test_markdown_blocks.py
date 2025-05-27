import unittest
from markdown_blocks import *


class TestMarkdownToHTML(unittest.TestCase):
    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_markdown_to_blocks_newlines(self):
        md = """
This is **bolded** paragraph




This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_markdown_block_to_blocktype_paragraph(self):
        block = """this is some text
also with a new line"""
        self.assertEqual(block_to_block_type(block), BlockType.paragraph)

    def test_markdown_block_to_blocktype_heading(self):
        block = "### This is a Heading"
        self.assertEqual(block_to_block_type(block), BlockType.heading)

    def test_markdown_block_to_blocktype_code(self):
        block = """```this is some code
also with a new line```"""
        self.assertEqual(block_to_block_type(block), BlockType.code)

    def test_markdown_block_to_blocktype_quote(self):
        block = """> this is a quote
> with multiple lines
>some without spaces"""
        self.assertEqual(block_to_block_type(block), BlockType.quote)
    
    def test_markdown_block_to_blocktype_unordered_list(self):
        block = """- this is a list
- with multiple lines
- all with spaces"""
        self.assertEqual(block_to_block_type(block), BlockType.unordered_list)

    def test_markdown_block_to_blocktype_ordered_list(self):
        block = """1. this is an ordered list
2. with multiple lines
3. all with spaces"""
        self.assertEqual(block_to_block_type(block), BlockType.ordered_list)


    #TESTS FOR MARKDOWN TO HTML NODES
    def test_paragraphs(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_codeblock(self):
        md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )


if __name__ == "__main__":
    unittest.main()
