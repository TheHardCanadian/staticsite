import unittest
from textnode import TextNode, TextType
from delimiter import split_nodes_delimiter, regex_find_image, regex_find_link, split_nodes_image, split_nodes_link

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

class TestRegexFunctions(unittest.TestCase):

    def test_regex_image(self):
        t1_single = regex_find_image("This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)")
        t2_duo = regex_find_image("This is a ![screenshot](https://example.com/images/screen.png) of my screen and also a ![profile pic](https://i.imgur.com/abc123.jpg)")
        t3_trio = regex_find_image("This is a ![screenshot](https://example.com/images/screen.png) of my screen and also a ![profile pic](https://i.imgur.com/abc123.jpg) and the ![company logo](https://cdn.company.com/logo.svg)")
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], t1_single)
        self.assertListEqual([("screenshot", "https://example.com/images/screen.png"),("profile pic", "https://i.imgur.com/abc123.jpg")], t2_duo)
        self.assertListEqual([("screenshot", "https://example.com/images/screen.png"),("profile pic", "https://i.imgur.com/abc123.jpg"), ("company logo", "https://cdn.company.com/logo.svg") ], t3_trio)

    def test_regex_link(self):
        t1_single = regex_find_link("This is text with an [image](https://i.imgur.com/zjjcJKZ.png)")
        t2_duo = regex_find_link("This is a [screenshot](https://example.com/images/screen.png) of my screen and also a [profile pic](https://i.imgur.com/abc123.jpg)")
        t3_trio = regex_find_link("This is a [screenshot](https://example.com/images/screen.png) of my screen and also a [profile pic](https://i.imgur.com/abc123.jpg) and the [company logo](https://cdn.company.com/logo.svg)")
        t4_no_url = regex_find_link("This is a [screenshot] of my screen and also a [profile pic] and the [company logo]")

        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], t1_single)
        self.assertListEqual([("screenshot", "https://example.com/images/screen.png"),("profile pic", "https://i.imgur.com/abc123.jpg")], t2_duo)
        self.assertListEqual([("screenshot", "https://example.com/images/screen.png"),("profile pic", "https://i.imgur.com/abc123.jpg"), ("company logo", "https://cdn.company.com/logo.svg") ], t3_trio)
        #self.assertListEqual([("screenshot"),("profile pic"), ("company logo") ], t4_no_url)


class TestSplitNodes(unittest.TestCase):
    def test_split_image(self):
        node = TextNode (
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
        TextType.PLAIN_TEXT,
        )
        
        new_nodes = split_nodes_image(node.text, regex_find_image)

        self.assertListEqual([
            TextNode("This is text with an ", TextType.PLAIN_TEXT),
            TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
            TextNode(" and another ", TextType.PLAIN_TEXT),
            TextNode("second image", TextType.IMAGE,"https://i.imgur.com/3elNhQu.png"),
        ], new_nodes)

        node = TextNode (
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png) and some following text",
        TextType.PLAIN_TEXT,
        )
        
        new_nodes = split_nodes_image(node.text, regex_find_image)

        self.assertListEqual([
            TextNode("This is text with an ", TextType.PLAIN_TEXT),
            TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
            TextNode(" and another ", TextType.PLAIN_TEXT),
            TextNode("second image", TextType.IMAGE,"https://i.imgur.com/3elNhQu.png"),
            TextNode(" and some following text", TextType.PLAIN_TEXT),
        ], new_nodes)
        
        node = TextNode (
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png) and some following text and a ![third image](https://i.imgur.com/3elNhQu.png)![fourth image](https://i.imgur.com/3elNhQu.png)",
        TextType.PLAIN_TEXT,
        )
        
        new_nodes = split_nodes_image(node.text, regex_find_image)

        self.assertListEqual([
            TextNode("This is text with an ", TextType.PLAIN_TEXT),
            TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
            TextNode(" and another ", TextType.PLAIN_TEXT),
            TextNode("second image", TextType.IMAGE,"https://i.imgur.com/3elNhQu.png"),
            TextNode(" and some following text and a ", TextType.PLAIN_TEXT),
            TextNode("third image", TextType.IMAGE,"https://i.imgur.com/3elNhQu.png"),
            TextNode("", TextType.PLAIN_TEXT),
            TextNode("fourth image", TextType.IMAGE,"https://i.imgur.com/3elNhQu.png")
        ], new_nodes)



        #node = TextNode (
        #    "This is text with an image that has no text, just url ![](https://i.imgur.com/zjjcJKZ.png)",
        #TextType.PLAIN_TEXT,
        #)
        
        #new_nodes = split_nodes_link(node.text, regex_find_link)

        #self.assertListEqual([
        #    TextNode("This is text with an image that has no text, just url ", TextType.PLAIN_TEXT),
        #    TextNode("", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
            
        #], new_nodes
        #)

    def test_split_link(self):
        node = TextNode (
            "This is text with a [link](https://i.imgur.com/zjjcJKZ.png) and another [link](https://i.imgur.com/3elNhQu.png)",
        TextType.PLAIN_TEXT,
        )
        
        new_nodes = split_nodes_link(node.text, regex_find_link)

        self.assertListEqual([
            TextNode("This is text with a ", TextType.PLAIN_TEXT),
            TextNode("link", TextType.LINK, "https://i.imgur.com/zjjcJKZ.png"),
            TextNode(" and another ", TextType.PLAIN_TEXT),
            TextNode("link", TextType.LINK,"https://i.imgur.com/3elNhQu.png"),
        ], new_nodes)

        node = TextNode (
            "This is text with a [link](https://i.imgur.com/zjjcJKZ.png) and another [link](https://i.imgur.com/3elNhQu.png) and some following text",
        TextType.PLAIN_TEXT,
        )
        
        new_nodes = split_nodes_link(node.text, regex_find_link)

        self.assertListEqual([
            TextNode("This is text with a ", TextType.PLAIN_TEXT),
            TextNode("link", TextType.LINK, "https://i.imgur.com/zjjcJKZ.png"),
            TextNode(" and another ", TextType.PLAIN_TEXT),
            TextNode("link", TextType.LINK,"https://i.imgur.com/3elNhQu.png"),
            TextNode(" and some following text", TextType.PLAIN_TEXT),
        ], new_nodes)
        
        node = TextNode (
            "This is text with a [link](https://i.imgur.com/zjjcJKZ.png) and another [second link](https://i.imgur.com/3elNhQu.png) and some following text and a [third link](https://i.imgur.com/3elNhQu.png)[fourth link](https://i.imgur.com/3elNhQu.png)",
        TextType.PLAIN_TEXT,
        )
        
        new_nodes = split_nodes_link(node.text, regex_find_link)

        self.assertListEqual([
            TextNode("This is text with a ", TextType.PLAIN_TEXT),
            TextNode("link", TextType.LINK, "https://i.imgur.com/zjjcJKZ.png"),
            TextNode(" and another ", TextType.PLAIN_TEXT),
            TextNode("second link", TextType.LINK,"https://i.imgur.com/3elNhQu.png"),
            TextNode(" and some following text and a ", TextType.PLAIN_TEXT),
            TextNode("third link", TextType.LINK,"https://i.imgur.com/3elNhQu.png"),
            TextNode("", TextType.PLAIN_TEXT),
            TextNode("fourth link", TextType.LINK,"https://i.imgur.com/3elNhQu.png")
        ], new_nodes)

        #node = TextNode (
        #    "This is text with a link that has no text, just url [](https://i.imgur.com/zjjcJKZ.png)",
        #TextType.PLAIN_TEXT,
        #)
        
        #new_nodes = split_nodes_link(node.text, regex_find_link)

        #self.assertListEqual([
        #    TextNode("This is text with a link that has no text, just url ", TextType.PLAIN_TEXT),
        #    TextNode("", TextType.LINK, "https://i.imgur.com/zjjcJKZ.png"),
            
        #], new_nodes
    #)


"""

 node = TextNode(
        "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
        TextType.TEXT,
    )
    new_nodes = split_nodes_image([node])
    self.assertListEqual(
        [
            TextNode("This is text with an ", TextType.TEXT),
            TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
            TextNode(" and another ", TextType.TEXT),
            TextNode(
                "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
            ),
        ],
        new_nodes,
    )
# Image tuples

[("profile pic", "https://i.imgur.com/abc123.jpg")]
[("screenshot", "https://example.com/images/screen.png")]
[("company logo", "https://cdn.company.com/logo.svg")]
[("chart", "https://data.viz/chart-2024.gif")]
[("avatar", "https://assets.site.com/user/avatar.webp")]

# Link tuples  
[("Boot Dev", "https://www.boot.dev")]
[("GitHub repo", "https://github.com/user/project")]
[("documentation", "https://docs.python.org/3/")]
[("tutorial", "https://www.youtube.com/watch?v=dQw4w9WgXcQ")]
[("portfolio", "https://mysite.dev/projects")]

"""

if __name__ == "__main__":
    unittest.main() 