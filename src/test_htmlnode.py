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
    

if __name__ == "__main__":
    unittest.main()