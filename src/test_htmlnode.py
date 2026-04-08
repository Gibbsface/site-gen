import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode

class TestTextNode(unittest.TestCase):
    def test_empty(self):
        node = HTMLNode()
        self.assertEqual(str(node), "HTMLNode(None, None, None, None)")

    def test_full(self):
        node = HTMLNode("h1", "dummy text", [HTMLNode()], {"href": "www.dts.edu"})
        self.assertEqual(str(node), "HTMLNode(h1, dummy text, [HTMLNode(None, None, None, None)], {'href': 'www.dts.edu'})")

    def test_props_to_html(self):
        node = HTMLNode("h1", "dummy text", [HTMLNode()], {"href": "www.dts.edu"})
        dummy = node.props_to_html()
        self.assertEqual(dummy, " href=\"www.dts.edu\"")

    def test_p_to_html(self):
        node_html = LeafNode("p", "This is a paragraph.").to_html()
        dummy = "<p>This is a paragraph.</p>"
        self.assertEqual(node_html, dummy)

    def test_a_to_html(self):
        node_html = LeafNode("a", "Click me!", {"href": "https://www.google.com"}).to_html()
        dummy = "<a href=\"https://www.google.com\">Click me!</a>"
        self.assertEqual(node_html, dummy)

    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

if __name__ == "__main__":
    unittest.main()