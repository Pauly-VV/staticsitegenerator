import unittest

from textnode import *
from split_nodes_delimiter import *

class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", "bold")
        node2 = TextNode("This is a text node", "bold")
        self.assertEqual(node, node2)

    def test2_eq(self):
        node = TextNode("123 Test Text", "bold", "www.something.com")
        node2 = TextNode("123 Test Text", "bold", "www.something.com")
        self.assertEqual(node, node2)

    def test3_eq(self):
        node = TextNode("", "", "")
        node2 = TextNode("", "", "")
        self.assertEqual(node, node2)
    
    def test4_NOTeq(self):
        node = TextNode("123 Test Text", "bold", "www.something.com")
        node2 = TextNode("123 Test Text", "italics", "www.something.com")
        self.assertNotEqual(node, node2)

    def test_repr(self):
        node = TextNode("This is a text node", TextType.TEXT, "https://www.boot.dev")
        self.assertEqual(
            "TextNode(This is a text node, TextType.TEXT, https://www.boot.dev)", repr(node)
        )

class TestTextNodetoHTMLNode(unittest.TestCase):
    def test_conversion(self):
        textNodeTest = TextNode("This is some text", TextType.BOLD)
        htmltestNode = text_node_to_html_node(textNodeTest)
        self.assertEqual(htmltestNode.tag, "b")
        self.assertEqual(htmltestNode.value, "This is some text")

    def test_img_conversion(self):
        test_node = TextNode("image description", TextType.IMAGE, "www.image.url")
        html_test_node = text_node_to_html_node(test_node)
        self.assertEqual(html_test_node.tag, "img")
        self.assertEqual(html_test_node.value, "")
        self.assertEqual(html_test_node.props, {"src":"www.image.url", "alt":"image description"})

    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

class TestSplitNodesDelimiter(unittest.TestCase):
    def test_Code_conversion(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        actual = [TextNode("This is text with a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" word", TextType.TEXT),]
        self.assertEqual(new_nodes, actual)

    def test_Bold_conversion(self):
        node = TextNode("This is text with a **bold** word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        actual = [TextNode("This is text with a ", TextType.TEXT),
                TextNode("bold", TextType.BOLD),
                TextNode(" word", TextType.TEXT),]
        self.assertEqual(new_nodes, actual)

    def test_multiple_delim_conversion(self):
        node = TextNode("This is text with a **bold** word and an *italic* word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        newer_nodes = split_nodes_delimiter(new_nodes, "*", TextType.ITALIC)
        actual = [TextNode("This is text with a ", TextType.TEXT),
                TextNode("bold", TextType.BOLD),
                TextNode(" word and an ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word", TextType.TEXT),]
        self.assertEqual(newer_nodes, actual)

    def test_multiple_bold_ending_delim_conversion(self):
        node = TextNode("This is text with a **bold** word and **another word**", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        actual = [TextNode("This is text with a ", TextType.TEXT),
                TextNode("bold", TextType.BOLD),
                TextNode(" word and ", TextType.TEXT),
                TextNode("another word", TextType.BOLD),]
        self.assertEqual(new_nodes, actual)

    


if __name__ == "__main__":
    unittest.main()