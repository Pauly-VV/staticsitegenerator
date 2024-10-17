import unittest

from htmlnode import *

class TestHTMLNode(unittest.TestCase):
    def test_eq(self):
        node = HTMLNode("test_tag", "test_body_text", ["test_list_node","test_list_node2"], {"test":"test_attribute"})
        node2 = HTMLNode("test_tag", "test_body_text", ["test_list_node","test_list_node2"], {"test":"test_attribute"})
        self.assertEqual(node, node2)

    def test_Noteq(self):
        node = HTMLNode("test_tag", "test_body_text", ["test_list_node","test_list_node2"], {"test":"test_attribute"})
        node2 = HTMLNode("test_different_tag", "test_body_text", ["test_list_node","test_list_node2"], {"test":"test_attribute"})
        self.assertNotEqual(node, node2)

    def test_repr(self):
        node = HTMLNode("test_tag", "test_body_text", ["test_list_node","test_list_node2"], {"test":"test_attribute"})
        self.assertEqual(
            'HTMLNode:\ntag = test_tag \nvalue = test_body_text \nchildren = ["test_list_node", "test_list_node2"] \nprops =  test="test_attribute"', repr(node)
        )

    def test_parent_leaf_node_eq(self):
        node = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )
        result = "<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>"
        self.assertEqual(node.to_html(), result)

    def test_parent_leaf_node_nested_eq(self):
        node = ParentNode(
            "p", 
            [
                ParentNode(
                    "u", 
                    [LeafNode("b", "Bold text"), 
                     LeafNode(None, "Normal text")
                     ]
                ), 
                LeafNode("i", "italic text"), 
                LeafNode(None, "Normal text"),
            ],
        )
        result = "<p><u><b>Bold text</b>Normal text</u><i>italic text</i>Normal text</p>"
        self.assertEqual(node.to_html(), result)

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")


class TestLeafNode(unittest.TestCase):
    def test_eq(self):
        node = LeafNode("test_tag", "test_body_text", {"test":"test_attribute"})
        node2 = LeafNode("test_tag", "test_body_text", {"test":"test_attribute"})
        self.assertEqual(node, node2)

    def test_Noteq(self):
        node = LeafNode("test_tag", "test_body_text", {"test":"test_attribute"})
        node2 = LeafNode("test_different_tag", "test_body_text", {"test":"test_attribute"})
        self.assertNotEqual(node, node2)

    def test_repr(self):
        node = LeafNode("test_tag", "test_body_text", {"test":"test_attribute"})
        self.assertEqual(
            'HTMLNode:\ntag = test_tag \nvalue = test_body_text \nprops =  test="test_attribute"', repr(node)
        )
    
    def test_to_html_no_children(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_to_html_no_tag(self):
        node = LeafNode(None, "Hello, world!")
        self.assertEqual(node.to_html(), "Hello, world!")
    

if __name__ == "__main__":
    unittest.main()