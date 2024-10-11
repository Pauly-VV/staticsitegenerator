import unittest

from textnode import *

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
    
    def test4_eq(self):
        node = TextNode("123 Test Text", "bold", "www.something.com")
        node2 = TextNode("123 Test Text", "italics", "www.something.com")
        self.assertNotEqual(node, node2)

    def test_repr(self):
        node = TextNode("This is a text node", text_type_text, "https://www.boot.dev")
        self.assertEqual(
            "TextNode(This is a text node, text, https://www.boot.dev)", repr(node)
        )
    

if __name__ == "__main__":
    unittest.main()