import unittest

from textnode import TextNode, TextType
from delimiter import split_nodes_delimiter

class TestTextNode(unittest.TestCase):
    def test_eq_bold(self):
        node = TextNode("This is a text node", TextType.BOLD_TEXT)
        node2 = TextNode("This is a text node", TextType.BOLD_TEXT)
        self.assertEqual(node,node2)

    def test_eq_plain(self):
        node = TextNode("This is a text node", TextType.PLAIN_TEXT)
        node2 = TextNode("This is a text node", TextType.PLAIN_TEXT)
        self.assertEqual(node,node2)

    
    def test_eq_italic(self):
        node = TextNode("This is a text node", TextType.ITALIC_TEXT)
        node2 = TextNode("This is a text node", TextType.ITALIC_TEXT)
        self.assertEqual(node,node2)

    def test_eq_code(self):
        node = TextNode("This is a text node", TextType.CODE_TEXT)
        node2 = TextNode("This is a text node", TextType.CODE_TEXT)
        self.assertEqual(node,node2)

    def test_eq_link(self):
        node = TextNode("This is a text node", TextType.LINK)
        node2 = TextNode("This is a text node", TextType.LINK)
        self.assertEqual(node,node2)

    def test_eq_image(self):
        node = TextNode("This is a text node", TextType.IMAGE)
        node2 = TextNode("This is a text node", TextType.IMAGE)
        self.assertEqual(node,node2)

    def test_url_default(self):
        node = TextNode("This is a text node", TextType.LINK)
        self.assertEqual(node.url,None)

    def test_neq_image(self):
        node = TextNode("This is a text node", TextType.IMAGE)
        node2 = TextNode("This is a text node", TextType.BOLD_TEXT)
        self.assertNotEqual(node,node2)





class TestDelimiter(unittest.TestCase):
    # old_nodes_mid= "This is the text that I'm trying to {ACTION edit} for the test cycle"
    # old_nodes_start= "{ACTION. This is the text}  that I'm trying to edit for the test cycle"
    # old_nodes_end= "This is the text that I'm trying to edit for the test cycle {ACTION}"
    # old_nodes_multi= "This is {ACTIONthe text} that I'm trying to {ACTION edit} for the test cycle"
    #
    #
    #
    #
    #
    def test_delim_improper(self):
        #regex allows you to compare the message as well as the Exception being raised
        with self.assertRaisesRegex(Exception, r'Delimiter error: Improper delimiter'): 
            split_nodes_delimiter("This is the text that I'm trying to *(ACTION edit) for the test cycle", "*(", TextType.ITALIC_TEXT)

    def test_closedelim_notsupported(self):
        with self.assertRaisesRegex(KeyError, r'Text type italic does not support closing delimiters'): 
            split_nodes_delimiter("This is the text that I'm trying to _ACTION edit) for the test cycle", "_", TextType.ITALIC_TEXT, ")")


    def test_closedelim_improper(self):
        with self.assertRaisesRegex(Exception, r'Delimiter error: Improper closing delimiter'): 
            split_nodes_delimiter("This is the text that I'm trying to ![ACTION** edit) for the test cycle", "![", TextType.IMAGE, "**")

    def test_delim_improper_order(self):
        with self.assertRaisesRegex(Exception, r'Delimeter error: Closing delimeter not lead by opening delimeter'): 
            split_nodes_delimiter("This is the text that I'm trying to ]ACTION edit![ for the test cycle", "![", TextType.IMAGE, "]")
        with self.assertRaisesRegex(Exception, r'Delimeter error: Delimeter not followed by closing delimeter'): 
            split_nodes_delimiter("This is the text that I'm trying to ![ACTION edit![ for the test cycle", "![", TextType.IMAGE, "]")
    
    def test_bold(self):
        bold_mid = split_nodes_delimiter("This is the text that I'm trying to **ACTION edit** for the test cycle", "**", TextType.BOLD_TEXT)
        bold_mid2 = split_nodes_delimiter("This is the text that I'm trying to __ACTION edit__ for the test cycle", "__", TextType.BOLD_TEXT)
        self.assertEqual(bold_mid, [TextNode("This is the text that I'm trying to ", TextType.PLAIN_TEXT), TextNode("ACTION edit", TextType.BOLD_TEXT), TextNode(" for the test cycle", TextType.PLAIN_TEXT)])
        self.assertEqual(bold_mid2, [TextNode("This is the text that I'm trying to ", TextType.PLAIN_TEXT), TextNode("ACTION edit", TextType.BOLD_TEXT), TextNode(" for the test cycle", TextType.PLAIN_TEXT)])
        
        bold_start = split_nodes_delimiter("**This is the text** that I'm trying to edit for the test cycle", "**", TextType.BOLD_TEXT)
        bold_start2 = split_nodes_delimiter("__This is the text__ that I'm trying to edit for the test cycle", "__", TextType.BOLD_TEXT) 
        self.assertEqual(bold_start, [TextNode("This is the text", TextType.BOLD_TEXT), TextNode(" that I'm trying to edit for the test cycle", TextType.PLAIN_TEXT)])
        self.assertEqual(bold_start2, [TextNode("This is the text", TextType.BOLD_TEXT), TextNode(" that I'm trying to edit for the test cycle", TextType.PLAIN_TEXT)])
        
        bold_end = split_nodes_delimiter("This is the text that I'm trying to edit for the **test cycle**", "**", TextType.BOLD_TEXT)
        bold_end2 = split_nodes_delimiter("This is the text that I'm trying to edit for the __test cycle__", "__", TextType.BOLD_TEXT)
        self.assertEqual(bold_end, [TextNode("This is the text that I'm trying to edit for the ", TextType.PLAIN_TEXT), TextNode("test cycle", TextType.BOLD_TEXT)])
        self.assertEqual(bold_end2, [TextNode("This is the text that I'm trying to edit for the ", TextType.PLAIN_TEXT), TextNode("test cycle", TextType.BOLD_TEXT)])

        bold_multi = split_nodes_delimiter("This is the text **that I'm trying** to edit for the **test cycle**", "**", TextType.BOLD_TEXT)
        bold_multi2 = split_nodes_delimiter("This is the text __that I'm trying__ to edit for the __test cycle__", "__", TextType.BOLD_TEXT)
        self.assertEqual(bold_multi, [TextNode("This is the text ", TextType.PLAIN_TEXT), TextNode("that I'm trying",TextType.BOLD_TEXT), TextNode(" to edit for the ", TextType.PLAIN_TEXT), TextNode("test cycle", TextType.BOLD_TEXT)])
        self.assertEqual(bold_multi2, [TextNode("This is the text ", TextType.PLAIN_TEXT), TextNode("that I'm trying",TextType.BOLD_TEXT), TextNode(" to edit for the ", TextType.PLAIN_TEXT), TextNode("test cycle", TextType.BOLD_TEXT)])


    def test_italic(self):
        bold_mid = split_nodes_delimiter("This is the text that I'm trying to *ACTION edit* for the test cycle", "*", TextType.ITALIC_TEXT)
        bold_mid2 = split_nodes_delimiter("This is the text that I'm trying to _ACTION edit_ for the test cycle", "_", TextType.ITALIC_TEXT)
        self.assertEqual(bold_mid, [TextNode("This is the text that I'm trying to ", TextType.PLAIN_TEXT), TextNode("ACTION edit", TextType.ITALIC_TEXT), TextNode(" for the test cycle", TextType.PLAIN_TEXT)])
        self.assertEqual(bold_mid2, [TextNode("This is the text that I'm trying to ", TextType.PLAIN_TEXT), TextNode("ACTION edit", TextType.ITALIC_TEXT), TextNode(" for the test cycle", TextType.PLAIN_TEXT)])
        
        bold_start = split_nodes_delimiter("*This is the text* that I'm trying to edit for the test cycle", "*", TextType.ITALIC_TEXT)
        bold_start2 = split_nodes_delimiter("_This is the text_ that I'm trying to edit for the test cycle", "_", TextType.ITALIC_TEXT) 
        self.assertEqual(bold_start, [TextNode("This is the text", TextType.ITALIC_TEXT), TextNode(" that I'm trying to edit for the test cycle", TextType.PLAIN_TEXT)])
        self.assertEqual(bold_start2, [TextNode("This is the text", TextType.ITALIC_TEXT), TextNode(" that I'm trying to edit for the test cycle", TextType.PLAIN_TEXT)])
        
        bold_end = split_nodes_delimiter("This is the text that I'm trying to edit for the *test cycle**", "*", TextType.ITALIC_TEXT)
        bold_end2 = split_nodes_delimiter("This is the text that I'm trying to edit for the _test cycle_", "_", TextType.ITALIC_TEXT)
        self.assertEqual(bold_end, [TextNode("This is the text that I'm trying to edit for the ", TextType.PLAIN_TEXT), TextNode("test cycle", TextType.ITALIC_TEXT)])
        self.assertEqual(bold_end2, [TextNode("This is the text that I'm trying to edit for the ", TextType.PLAIN_TEXT), TextNode("test cycle", TextType.ITALIC_TEXT)])

        bold_multi = split_nodes_delimiter("This is the text *that I'm trying* to edit for the *test cycle*", "*", TextType.ITALIC_TEXT)
        bold_multi2 = split_nodes_delimiter("This is the text _that I'm trying_ to edit for the _test cycle_", "_", TextType.ITALIC_TEXT)
        self.assertEqual(bold_multi, [TextNode("This is the text ", TextType.PLAIN_TEXT), TextNode("that I'm trying",TextType.ITALIC_TEXT), TextNode(" to edit for the ", TextType.PLAIN_TEXT), TextNode("test cycle", TextType.ITALIC_TEXT)])
        self.assertEqual(bold_multi2, [TextNode("This is the text ", TextType.PLAIN_TEXT), TextNode("that I'm trying",TextType.ITALIC_TEXT), TextNode(" to edit for the ", TextType.PLAIN_TEXT), TextNode("test cycle", TextType.ITALIC_TEXT)])     
    

    def test_codetext(self):
            code_mid = split_nodes_delimiter("This is the text that I'm trying to `ACTION edit` for the test cycle", "`", TextType.CODE_TEXT)
            self.assertEqual(code_mid, [TextNode("This is the text that I'm trying to ", TextType.PLAIN_TEXT), TextNode("ACTION edit", TextType.CODE_TEXT), TextNode(" for the test cycle", TextType.PLAIN_TEXT)])
            
            code_start = split_nodes_delimiter("`This is the text` that I'm trying to edit for the test cycle", "`", TextType.CODE_TEXT)
            self.assertEqual(code_start, [TextNode("This is the text", TextType.CODE_TEXT), TextNode(" that I'm trying to edit for the test cycle", TextType.PLAIN_TEXT)])
            
            code_end = split_nodes_delimiter("This is the text that I'm trying to edit for the `test cycle`", "`", TextType.CODE_TEXT)
            self.assertEqual(code_end, [TextNode("This is the text that I'm trying to edit for the ", TextType.PLAIN_TEXT), TextNode("test cycle", TextType.CODE_TEXT)])

            code_multi = split_nodes_delimiter("This is the text `that I'm trying` to edit for the `test cycle`", "`", TextType.CODE_TEXT)
            self.assertEqual(code_multi, [TextNode("This is the text ", TextType.PLAIN_TEXT), TextNode("that I'm trying",TextType.CODE_TEXT), TextNode(" to edit for the ", TextType.PLAIN_TEXT), TextNode("test cycle", TextType.CODE_TEXT)])

    def test_image(self):
            image_mid = split_nodes_delimiter("This is the text that I'm trying to ![ACTION edit] for the test cycle", "![", TextType.IMAGE,"]")
            self.assertEqual(image_mid, [TextNode("This is the text that I'm trying to ", TextType.PLAIN_TEXT), TextNode("ACTION edit", TextType.IMAGE), TextNode(" for the test cycle", TextType.PLAIN_TEXT)])
            
            image_start = split_nodes_delimiter("![This is the text] that I'm trying to edit for the test cycle", "![", TextType.IMAGE, "]")
            self.assertEqual(image_start, [TextNode("This is the text", TextType.IMAGE), TextNode(" that I'm trying to edit for the test cycle", TextType.PLAIN_TEXT)])
            
            image_end = split_nodes_delimiter("This is the text that I'm trying to edit for the ![test cycle]", "![", TextType.IMAGE, "]")
            self.assertEqual(image_end, [TextNode("This is the text that I'm trying to edit for the ", TextType.PLAIN_TEXT), TextNode("test cycle", TextType.IMAGE)])

            image_multi = split_nodes_delimiter("This is the text ![that I'm trying] to edit for the ![test cycle]", "![", TextType.IMAGE,"]")
            self.assertEqual(image_multi, [TextNode("This is the text ", TextType.PLAIN_TEXT), TextNode("that I'm trying",TextType.IMAGE), TextNode(" to edit for the ", TextType.PLAIN_TEXT), TextNode("test cycle", TextType.IMAGE)])

    def test_link(self):
            link_mid = split_nodes_delimiter("This is the text that I'm trying to [ACTION edit] for the test cycle", "[", TextType.LINK,"]")
            self.assertEqual(link_mid, [TextNode("This is the text that I'm trying to ", TextType.PLAIN_TEXT), TextNode("ACTION edit", TextType.LINK), TextNode(" for the test cycle", TextType.PLAIN_TEXT)])
            
            link_start = split_nodes_delimiter("[This is the text] that I'm trying to edit for the test cycle", "[", TextType.LINK, "]")
            self.assertEqual(link_start, [TextNode("This is the text", TextType.LINK), TextNode(" that I'm trying to edit for the test cycle", TextType.PLAIN_TEXT)])
            
            link_end = split_nodes_delimiter("This is the text that I'm trying to edit for the [test cycle]", "[", TextType.LINK, "]")
            self.assertEqual(link_end, [TextNode("This is the text that I'm trying to edit for the ", TextType.PLAIN_TEXT), TextNode("test cycle", TextType.LINK)])

            link_multi = split_nodes_delimiter("This is the text [that I'm trying] to edit for the [test cycle]", "[", TextType.LINK,"]")
            self.assertEqual(link_multi, [TextNode("This is the text ", TextType.PLAIN_TEXT), TextNode("that I'm trying",TextType.LINK), TextNode(" to edit for the ", TextType.PLAIN_TEXT), TextNode("test cycle", TextType.LINK)])
            

if __name__ == "__main__":
    unittest.main()