import unittest
from textnode import TextNode, TextType
from delimiter import split_nodes_delimiter, regex_find_image, regex_find_link, split_nodes_image, split_nodes_link, text_to_textnodes

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
    def setUp(self):
        self.maxDiff = None

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

    def test_textnode_full(self):
        
        #test 1:
        text1 = "This is **bold text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        nodes1 = text_to_textnodes(text1)
        self.assertListEqual([
            TextNode("This is ", TextType.PLAIN_TEXT),
            TextNode("bold text", TextType.BOLD_TEXT),
            TextNode(" with an ", TextType.PLAIN_TEXT),
            TextNode("italic", TextType.ITALIC_TEXT),
            TextNode(" word and a ", TextType.PLAIN_TEXT),
            TextNode("code block", TextType.CODE_TEXT),
            TextNode(" and an ", TextType.PLAIN_TEXT),
            TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
            TextNode(" and a ", TextType.PLAIN_TEXT),
            TextNode("link", TextType.LINK,"https://boot.dev"),
        ], nodes1)

        text2 = "This is **bold text** with an _italic_ word and a **second bold text** followed by a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        nodes2 = text_to_textnodes(text2)
        self.assertListEqual([
            TextNode("This is ", TextType.PLAIN_TEXT),
            TextNode("bold text", TextType.BOLD_TEXT),
            TextNode(" with an ", TextType.PLAIN_TEXT),
            TextNode("italic", TextType.ITALIC_TEXT),
            TextNode(" word and a ", TextType.PLAIN_TEXT),
            TextNode("second bold text", TextType.BOLD_TEXT),
            TextNode(" followed by a ", TextType.PLAIN_TEXT),
            TextNode("code block", TextType.CODE_TEXT),
            TextNode(" and an ", TextType.PLAIN_TEXT),
            TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
            TextNode(" and a ", TextType.PLAIN_TEXT),
            TextNode("link", TextType.LINK,"https://boot.dev"),
        ], nodes2)
        
        text3 = "This is **bold text** with an _italic_ word and a **second bold text** and a **third bold text** followed by a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        nodes3 = text_to_textnodes(text3)
        self.assertListEqual([
            TextNode("This is ", TextType.PLAIN_TEXT),
            TextNode("bold text", TextType.BOLD_TEXT),
            TextNode(" with an ", TextType.PLAIN_TEXT),
            TextNode("italic", TextType.ITALIC_TEXT),
            TextNode(" word and a ", TextType.PLAIN_TEXT),
            TextNode("second bold text", TextType.BOLD_TEXT),
            TextNode(" and a ", TextType.PLAIN_TEXT),
            TextNode("third bold text", TextType.BOLD_TEXT),
            TextNode(" followed by a ", TextType.PLAIN_TEXT),
            TextNode("code block", TextType.CODE_TEXT),
            TextNode(" and an ", TextType.PLAIN_TEXT),
            TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
            TextNode(" and a ", TextType.PLAIN_TEXT),
            TextNode("link", TextType.LINK,"https://boot.dev"),
        ], nodes3)
        
        
        text4 = "This is **bold text** with an _italic_ word and a _second italic word_ followed by a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev) with a _third italic word_"
        nodes4 = text_to_textnodes(text4)
        self.assertListEqual([
            TextNode("This is ", TextType.PLAIN_TEXT),
            TextNode("bold text", TextType.BOLD_TEXT),
            TextNode(" with an ", TextType.PLAIN_TEXT),
            TextNode("italic", TextType.ITALIC_TEXT),
            TextNode(" word and a ", TextType.PLAIN_TEXT),
            TextNode("second italic word", TextType.ITALIC_TEXT),
            TextNode(" followed by a ", TextType.PLAIN_TEXT),
            TextNode("code block", TextType.CODE_TEXT),
            TextNode(" and an ", TextType.PLAIN_TEXT),
            TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
            TextNode(" and a ", TextType.PLAIN_TEXT),
            TextNode("link", TextType.LINK,"https://boot.dev"),
            TextNode(" with a ", TextType.PLAIN_TEXT),
            TextNode("third italic word", TextType.ITALIC_TEXT),
        ], nodes4)
        
        text5 = "This is **bold text** with an _italic_ word and another _italic word_ along with a **second bold text** followed by a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a ![Qui-Gon Jinn image](https://en.wikipedia.org/wiki/Qui-Gon_Jinn#/media/File:Qui-Gon_Jinn.png) and a [link](https://boot.dev)"
        nodes5 = text_to_textnodes(text5)
        self.assertListEqual([
            TextNode("This is ", TextType.PLAIN_TEXT),
            TextNode("bold text", TextType.BOLD_TEXT),
            TextNode(" with an ", TextType.PLAIN_TEXT),
            TextNode("italic", TextType.ITALIC_TEXT),
            TextNode(" word and another ", TextType.PLAIN_TEXT),
            TextNode("italic word", TextType.ITALIC_TEXT),
            TextNode(" along with a ", TextType.PLAIN_TEXT),
            TextNode("second bold text", TextType.BOLD_TEXT),
            TextNode(" followed by a ", TextType.PLAIN_TEXT),
            TextNode("code block", TextType.CODE_TEXT),
            TextNode(" and an ", TextType.PLAIN_TEXT),
            TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
            TextNode(" and a ", TextType.PLAIN_TEXT),
            TextNode("Qui-Gon Jinn image", TextType.IMAGE, "https://en.wikipedia.org/wiki/Qui-Gon_Jinn#/media/File:Qui-Gon_Jinn.png"),
            TextNode(" and a ", TextType.PLAIN_TEXT),
            TextNode("link", TextType.LINK,"https://boot.dev"),
        ], nodes5)

        text6 = "This is **bold text** with an _italic_ word and another _italic word_ along with a **second bold text** followed by a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a ![Qui-Gon Jinn image] and a [link](https://boot.dev)"
        nodes6 = text_to_textnodes(text6)
        self.assertListEqual([
            TextNode("This is ", TextType.PLAIN_TEXT),
            TextNode("bold text", TextType.BOLD_TEXT),
            TextNode(" with an ", TextType.PLAIN_TEXT),
            TextNode("italic", TextType.ITALIC_TEXT),
            TextNode(" word and another ", TextType.PLAIN_TEXT),
            TextNode("italic word", TextType.ITALIC_TEXT),
            TextNode(" along with a ", TextType.PLAIN_TEXT),
            TextNode("second bold text", TextType.BOLD_TEXT),
            TextNode(" followed by a ", TextType.PLAIN_TEXT),
            TextNode("code block", TextType.CODE_TEXT),
            TextNode(" and an ", TextType.PLAIN_TEXT),
            TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
            TextNode(" and a ![Qui-Gon Jinn image] and a ", TextType.PLAIN_TEXT),
            TextNode("link", TextType.LINK,"https://boot.dev"),
        ], nodes6)


        text7 = "This is **bold text** with an _italic_ word and another _italic word_ along with a **second bold text** followed by a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a ![Qui-Gon Jinn image](https://en.wikipedia.org/wiki/Qui-Gon_Jinn#/media/File:Qui-Gon_Jinn.png) and a [link](https://boot.dev) also, a link to the [star wars official website](https://www.starwars.com/)"
        nodes7 = text_to_textnodes(text7)
        self.assertListEqual([
            TextNode("This is ", TextType.PLAIN_TEXT),
            TextNode("bold text", TextType.BOLD_TEXT),
            TextNode(" with an ", TextType.PLAIN_TEXT),
            TextNode("italic", TextType.ITALIC_TEXT),
            TextNode(" word and another ", TextType.PLAIN_TEXT),
            TextNode("italic word", TextType.ITALIC_TEXT),
            TextNode(" along with a ", TextType.PLAIN_TEXT),
            TextNode("second bold text", TextType.BOLD_TEXT),
            TextNode(" followed by a ", TextType.PLAIN_TEXT),
            TextNode("code block", TextType.CODE_TEXT),
            TextNode(" and an ", TextType.PLAIN_TEXT),
            TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
            TextNode(" and a ", TextType.PLAIN_TEXT),
            TextNode("Qui-Gon Jinn image", TextType.IMAGE, "https://en.wikipedia.org/wiki/Qui-Gon_Jinn#/media/File:Qui-Gon_Jinn.png"),
            TextNode(" and a ", TextType.PLAIN_TEXT),
            TextNode("link", TextType.LINK,"https://boot.dev"),
            TextNode(" also, a link to the ", TextType.PLAIN_TEXT),
            TextNode("star wars official website", TextType.LINK, "https://www.starwars.com/"),
        ], nodes7)
        

        # Empty string
        #text_empty = ""
        #nodes_empty = text_to_textnodes(text_empty)
        #self.assertListEqual([TextNode("", TextType.PLAIN_TEXT)], nodes_empty)
        
        
        #text6 = "[This is](https://en.wikipedia.org/wiki/Qui-Gon_Jinn) **bold text** with an _italic_ word and another _italic word_ along with a **second bold text** followed by a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a ![Qui-Gon Jinn image](https://en.wikipedia.org/wiki/Qui-Gon_Jinn#/media/File:Qui-Gon_Jinn.png) and a [link](https://boot.dev)"

        # Test 15: Advanced wrecker technology  
        #text15 = "Modern **smart wreckers** include ![Computer-Controlled Wrecker](https://tech.com/smart-wrecker.jpg) with _automated rigging systems_ developed by [Advanced Towing Tech](https://www.advancedtowtech.com) engineers using **AI-assisted** operations shown in ![Control Interface](https://ai-tow.com/interface.png) with _predictive maintenance_"
        #nodes15 = text_to_textnodes(text15)
        



#test - one of each
#test - 2-1-1-1-1
#test - 3-1-1-1-1 Scrambled
#test - 4-1-1-1-1 Sync + Scramble
#test - 1-2-1-1-1
#test - 1-1-3-1-1
#test - 1-1-1-3



if __name__ == "__main__":
    unittest.main() 