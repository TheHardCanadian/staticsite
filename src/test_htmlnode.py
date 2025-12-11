import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode
from textnode import TextNode, TextType

class TestHTMLNode(unittest.TestCase):
    def test_init_with_all_params(self):
        props = {"href": "https://www.google.com", "target": "_blank"}
        children = ["child1", "child2"]
        node = HTMLNode("a", "Google", children, props)
        
        self.assertEqual(node.tag, "a")
        self.assertEqual(node.value, "Google")
        self.assertEqual(node.children, children)
        self.assertEqual(node.props, props)
    
    def test_init_with_defaults(self):
        node = HTMLNode()
        
        self.assertIsNone(node.tag)
        self.assertIsNone(node.value)
        self.assertIsNone(node.children)
        self.assertIsNone(node.props)
    
    def test_init_partial_params(self):
        node = HTMLNode("p", "This is a paragraph")
        
        self.assertEqual(node.tag, "p")
        self.assertEqual(node.value, "This is a paragraph")
        self.assertIsNone(node.children)
        self.assertIsNone(node.props)
    
    def test_repr(self):
        props = {"class": "button"}
        node = HTMLNode("button", "Click me", None, props)
        expected = "HTML Node: 'button', Value: 'Click me', Children: 'None', Props: {'class': 'button'}"
        
        self.assertEqual(repr(node), expected)
    
    def test_to_html_raises_not_implemented(self):
        node = HTMLNode("div", "content")
        
        with self.assertRaises(NotImplementedError):
            node.to_html()
    
    def test_props_to_html_single_prop(self):
        node = HTMLNode()
        node.props = {"href": "https://www.example.com"}
        
        result = node.props_to_html()
        self.assertEqual(result, 'href="https://www.example.com"')
    
    def test_props_to_html_multiple_props(self):
        node = HTMLNode()
        node.props = {"href": "https://www.example.com", "target": "_blank", "class": "link"}
        
        result = node.props_to_html()
        # Note: order might vary depending on Python version, so we check if all parts are present
        self.assertIn('href="https://www.example.com"', result)
        self.assertIn('target="_blank"', result)
        self.assertIn('class="link"', result)
    
    def test_props_to_html_empty_props(self):
        node = HTMLNode()
        node.props = {}
        
        result = node.props_to_html()
        self.assertEqual(result, "")

class TestLeafNode(unittest.TestCase):
    def test_value_none(self):
        node = LeafNode("p",None )
        with self.assertRaises(ValueError):
            node.to_html()

    def test_tag_none(self):
        node = LeafNode(None, "this is the value")
        self.assertEqual(node.value, "this is the value")

    def test_value_noprops(self):
        node = LeafNode("p", "this is the value")
        self.assertEqual(node.to_html(), "<p>this is the value</p>")
        

    def test_leaftohtml_props(self):
        node = LeafNode("a", "Search the Web", {"href": "https://www.google.com"})
        self.assertEqual(node.to_html(), '<a href="https://www.google.com">Search the Web</a>')
    
class TestParentNode(unittest.TestCase):
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

    def test_to_html_props(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node], {"class": "container", "id": "main"})
        expected = '<div class="container" id="main"><span>child</span></div>'
        self.assertEqual(parent_node.to_html(), expected)

    def test_to_html_grandchild_props(self):
        child_node = LeafNode("b", "grandchild", {"class": "container", "id": "main"})
        parent_node = ParentNode("div", "")

    def test_to_html_grandchild_props(self):
        grandchild_node = LeafNode("b", "grandchild", {"class": "bold"})
        child_node = ParentNode("span", [grandchild_node], {"id": "middle"})
        parent_node = ParentNode("div", [child_node], {"class": "container"})
        expected = '<div class="container"><span id="middle"><b class="bold">grandchild</b></span></div>'
        self.assertEqual(parent_node.to_html(), expected)

    def test_to_html_no_tag(self):
        child_node = LeafNode( "p", "child")
        with self.assertRaises(ValueError):
            parent_node = ParentNode(None, [child_node])
            self.assertEqual(parent_node.to_html(), ValueError("tag is none"))

    def test_to_html_no_children(self):
        with self.assertRaises(ValueError):
            parent_node = ParentNode("div", None)
            parent_node.to_html()

class TestTextType(unittest.TestCase):
    def test_enum_values(self):
        self.assertEqual(TextType.PLAIN_TEXT.value, "plain")
        self.assertEqual(TextType.BOLD_TEXT.value, "bold")
        self.assertEqual(TextType.ITALIC_TEXT.value, "italic")
        self.assertEqual(TextType.CODE_TEXT.value, "code")
    
    def test_textnode_with_enum(self):
        node = TextNode("Bold text", TextType.BOLD_TEXT)
        self.assertEqual(node.text_type, TextType.BOLD_TEXT)

    def test_enum_comparison(self):
        node1 = TextNode("text", TextType.BOLD_TEXT)
        node2 = TextNode("text", TextType.BOLD_TEXT)
        self.assertEqual(node1,node2)

    def test_all_enum_members_exist(self):
        expected_types = {"PLAIN_TEXT", "BOLD_TEXT","ITALIC_TEXT", "CODE_TEXT", "IMAGE", "LINK"}
        actual_types = {member.name for member in TextType}
        self.assertEqual(actual_types, expected_types)

    def test_textnode_different_types_not_equal(self):
        """Test that TextNodes with different types are not equal"""
        node1 = TextNode("text", TextType.BOLD_TEXT)
        node2 = TextNode("text", TextType.ITALIC_TEXT)
        self.assertNotEqual(node1, node2)
    
    def test_textnode_with_url(self):
        """Test TextNode with URL parameter"""
        node = TextNode("link text", TextType.PLAIN_TEXT, "https://example.com")
        self.assertEqual(node.url, "https://example.com")
    
    def test_textnode_default_url(self):
        """Test TextNode has None as default URL"""
        node = TextNode("text", TextType.PLAIN_TEXT)
        self.assertIsNone(node.url)
    
    def test_textnode_repr(self):
        """Test TextNode string representation"""
        node = TextNode("test text", TextType.BOLD_TEXT, "https://example.com")
        # Adjust expected string based on your actual __repr__ implementation
        print(node)
        self.assertIn("TEST TEXT", repr(node))
        self.assertIn("BOLD", repr(node))
        
if __name__ == "__main__":
    unittest.main()