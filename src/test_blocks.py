import unittest
from textnode import TextNode, TextType
from blocks import split_blocks, BlockType, block_to_block_type, markdown_to_html, extract_markdown


class TestBlocks(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None  # Show full diff output
    
    def test_split_blocks_basic(self):
        """Test basic document splitting"""
        document = """This is a heading

This is a paragraph of text. It has some **bold** and _italic_ words inside of it.

- This is the first list item in a list block
- This is a list item
- This is another list item"""
        
        result = split_blocks(document)
        expected = [
            "This is a heading",
            "This is a paragraph of text. It has some **bold** and _italic_ words inside of it.",
            "- This is the first list item in a list block\n- This is a list item\n- This is another list item"
        ]
        self.assertEqual(result, expected)
    
    def test_split_blocks_with_leading_whitespace(self):
        """Test document with leading whitespace"""
        document = """      This is a heading

This is a paragraph of text.

- This is a list item"""
        
        result = split_blocks(document)
        expected = [
            "This is a heading",
            "This is a paragraph of text.",
            "- This is a list item"
        ]
        self.assertEqual(result, expected)
    
    def test_split_blocks_with_trailing_whitespace(self):
        """Test document with trailing whitespace"""
        document = """This is a heading      

This is a paragraph of text.    

- This is a list item   """
        
        result = split_blocks(document)
        expected = [
            "This is a heading",
            "This is a paragraph of text.",
            "- This is a list item"
        ]
        self.assertEqual(result, expected)
    
    def test_split_blocks_empty_string(self):
        """Test empty document"""
        document = ""
        result = split_blocks(document)
        expected = []
        self.assertEqual(result, expected)
    
    def test_split_blocks_only_whitespace(self):
        """Test document with only whitespace"""
        document = "   \n\n   \n\n   "
        result = split_blocks(document)
        expected = []
        self.assertEqual(result, expected)
    
    def test_split_blocks_single_block(self):
        """Test document with single block"""
        document = "This is just one paragraph with no line breaks."
        result = split_blocks(document)
        expected = ["This is just one paragraph with no line breaks."]
        self.assertEqual(result, expected)
    
    def test_split_blocks_multiple_empty_lines(self):
        """Test document with multiple consecutive empty lines"""
        document = """First block


Second block



Third block"""
        
        result = split_blocks(document)
        expected = [
            "First block",
            "Second block",
            "Third block"
        ]
        self.assertEqual(result, expected)
    
    def test_split_blocks_code_block(self):
        """Test document with code blocks"""
        document = """Here's some code:

```python
def hello():
    print("Hello World")
```

And here's more text."""
        
        result = split_blocks(document)
        expected = [
            "Here's some code:",
            "```python\ndef hello():\n    print(\"Hello World\")\n```",
            "And here's more text."
        ]
        self.assertEqual(result, expected)
    
    def test_split_blocks_markdown_headers(self):
        """Test document with various markdown headers"""
        document = """# Main Header

## Subheader

### Smaller Header

Regular paragraph text."""
        
        result = split_blocks(document)
        expected = [
            "# Main Header",
            "## Subheader", 
            "### Smaller Header",
            "Regular paragraph text."
        ]
        self.assertEqual(result, expected)
    
    def test_split_blocks_lists(self):
        """Test document with different list types"""
        document = """Unordered list:

- Item 1
- Item 2
- Item 3

Ordered list:

1. First item
2. Second item
3. Third item

More text after lists."""
        
        result = split_blocks(document)
        expected = [
            "Unordered list:",
            "- Item 1\n- Item 2\n- Item 3",
            "Ordered list:",
            "1. First item\n2. Second item\n3. Third item",
            "More text after lists."
        ]
        self.assertEqual(result, expected)
    
    def test_split_blocks_quotes(self):
        """Test document with blockquotes"""
        document = """Here's a quote:

> This is a blockquote
> It spans multiple lines
> And has more content

Back to regular text."""
        
        result = split_blocks(document)
        expected = [
            "Here's a quote:",
            "> This is a blockquote\n> It spans multiple lines\n> And has more content",
            "Back to regular text."
        ]
        self.assertEqual(result, expected)
    
    def test_split_blocks_mixed_content(self):
        """Test document with mixed content types"""
        document = """# Document Title

This is an introduction paragraph with **bold** text.

## Code Example

```javascript
function greet(name) {
    return `Hello, ${name}!`;
}
```

### Features List

- Easy to use
- Well documented
- Fast performance

> Remember: Always test your code!

Final paragraph with _italic_ text."""
        
        result = split_blocks(document)
        expected = [
            "# Document Title",
            "This is an introduction paragraph with **bold** text.",
            "## Code Example",
            "```javascript\nfunction greet(name) {\n    return `Hello, ${name}!`;\n}\n```",
            "### Features List",
            "- Easy to use\n- Well documented\n- Fast performance",
            "> Remember: Always test your code!",
            "Final paragraph with _italic_ text."
        ]
        self.assertEqual(result, expected)
    
    def test_split_blocks_preserve_internal_newlines(self):
        """Test that single newlines within blocks are preserved"""
        document = """Block with
internal newlines
that should stay

Another block with
more internal
newlines"""
        
        result = split_blocks(document)
        expected = [
            "Block with\ninternal newlines\nthat should stay",
            "Another block with\nmore internal\nnewlines"
        ]
        self.assertEqual(result, expected)
    
    def test_split_blocks_edge_case_spacing(self):
        """Test edge cases with various spacing scenarios"""
        document = """   Leading spaces

    Tab at start

Trailing spaces   

    Mixed	spacing	

Normal text"""
        
        result = split_blocks(document)
        expected = [
            "Leading spaces",
            "Tab at start", 
            "Trailing spaces",
            "Mixed	spacing",
            "Normal text"
        ]
        self.assertEqual(result, expected)
    
    def test_split_blocks_return_type(self):
        """Test that function returns a list"""
        document = "Simple test"
        result = split_blocks(document)
        self.assertIsInstance(result, list)
        self.assertEqual(len(result), 1)
        self.assertIsInstance(result[0], str)

class TestMarkdowntoBlocks(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None  # Show full diff output

    def test_header1(self):
        # test header 1 that returns a header
        block = "#  A Tale of Two Cities"

        result = block_to_block_type(block)

        expected = BlockType.HEADING
        self.assertEqual(result, expected)

    def test_header2(self):
        # test header 1 that returns a header
        block = "##  A Tale of Two Cities"

        result = block_to_block_type(block)

        expected = BlockType.HEADING
        self.assertEqual(result, expected)
    
    def test_header3(self):
        # test header 1 that returns a header
        block = "###  A Tale of Two Cities"

        result = block_to_block_type(block)

        expected = BlockType.HEADING
        self.assertEqual(result, expected)

    def test_header4(self):
        # test header 1 that returns a header
        block = "####  A Tale of Two Cities"

        result = block_to_block_type(block)

        expected = BlockType.HEADING
        self.assertEqual(result, expected)

    def test_header5(self):
        # test header 5 that returns a header
        block = "#####  A Tale of Two Cities"

        result = block_to_block_type(block)

        expected = BlockType.HEADING
        self.assertEqual(result, expected)
    
    def test_header6(self):
        # test header 1 that returns a header
        block = "######  A Tale of Two Cities"

        result = block_to_block_type(block)

        expected = BlockType.HEADING
        self.assertEqual(result, expected)

    def test_header_not(self):
    # test header 1 that returns a header
        block = "####### A Tale of Two Cities"

        result = block_to_block_type(block)

        expected = BlockType.PARAGRAPH
        self.assertEqual(result, expected)   

    def test_code(self):
    # test header 1 that returns a header
        block = "```\n this is the code ```\n"

        result = block_to_block_type(block)

        expected = BlockType.CODE
        self.assertEqual(result, expected)

    def test_quote(self):
    # test header 1 that returns a header
        block = "> my favorite book is a tale of two cities."

        result = block_to_block_type(block)

        expected = BlockType.QUOTE
        self.assertEqual(result, expected)

    def test_unordered(self):
    # test header 1 that returns a header
        block = """- a tale of two cities.
        - great expectations
        - a christmas carol"""

        result = block_to_block_type(block)

        expected = BlockType.UNORDERED_LIST
        #print(block)
        self.assertEqual(result, expected)

    def test_ordered(self):
    # test header 1 that returns a header
        block = """1. a tale of two cities.
        2. great expectations
        3. a christmas carol"""

        result = block_to_block_type(block)

        expected = BlockType.ORDERED_LIST
        #print(block)
        self.assertEqual(result, expected)

    def test_ordered(self):
    # test header 1 that returns a header
        block = """1. a tale of two cities.
        2. great expectations
        3. a christmas carol"""

        result = block_to_block_type(block)

        expected = BlockType.ORDERED_LIST
        #print(block)
        self.assertEqual(result, expected)

    def test_paragraph(self):
    # test header 1 that returns a header
        block = """This is finna be a paragraph a tale of two cities.
        2. great expectations
        3. a christmas carol"""

        result = block_to_block_type(block)

        expected = BlockType.PARAGRAPH
        print(block)
        self.assertEqual(result, expected)
    

    def test_html_paragraph(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

"""

        node = markdown_to_html(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p></div>",
        )

    def test_html_paragraphs(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""

        node = markdown_to_html(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_html_lists(self):
        md = """
- This is a list
- with items
- and _more_ items

1. This is an `ordered` list
2. with items
3. and more items

"""

        node = markdown_to_html(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ul><li>This is a list</li><li>with items</li><li>and <i>more</i> items</li></ul><ol><li>This is an <code>ordered</code> list</li><li>with items</li><li>and more items</li></ol></div>",
        )

    def test_html_headings(self):
        md = """
# this is an h1

this is paragraph text

## this is an h2
"""

        node = markdown_to_html(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h1>this is an h1</h1><p>this is paragraph text</p><h2>this is an h2</h2></div>",
        )

    def test_html_blockquote(self):
        md = """
> This is a
> blockquote block

this is paragraph text

"""

        node = markdown_to_html(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><blockquote>This is a blockquote block</blockquote><p>this is paragraph text</p></div>",
        )


class TestExtractHeaderTitle(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None  # Show full diff output

    def test_markdown_title(self):
        markdown = """# Main Title - This is an H1 Header

This is some introductory text under the main title. It contains regular paragraphs and some **bold text** and *italic text*.

## Section One - H2 Header

Here's content under the first section. This section talks about various topics.

### Subsection A - H3 Header

More detailed content here with some code examples:

```python
def hello_world():
    print("Hello, World!")
```

## Section Two - H2 Header

Another section with different content. This one has a list:

- Item one
- Item two  
- Item three

### Subsection B - H3 Header

# Another H1 Header in the Middle

This demonstrates multiple H1 headers in the same document.

Some text with a [link](https://example.com) and an image reference.

## Final Section

#NotAHeader - this line doesn't start with # at beginning
  # This is indented, so not a proper header

# Last H1 Header

Final content goes here.

## Conclusion

That's the end of our sample markdown file!"""

        result = extract_markdown(markdown)
        expected = "Main Title - This is an H1 Header"
        self.assertEqual(result, expected)

    def test_markdown_midtitle(self):
        markdown = """## Not Main Title - This is an H1 Header

This is some introductory text under the main title. It contains regular paragraphs and some **bold text** and *italic text*.

## Section One - H2 Header

Here's content under the first section. This section talks about various topics.

### Subsection A - H3 Header

More detailed content here with some code examples:

```python
def hello_world():
    print("Hello, World!")
```

## Section Two - H2 Header

Another section with different content. This one has a list:

- Item one
- Item two  
- Item three

### Subsection B - H3 Header

# Another H1 Header in the Middle - Should be Title

This demonstrates multiple H1 headers in the same document.

Some text with a [link](https://example.com) and an image reference.

## Final Section

#NotAHeader - this line doesn't start with # at beginning
  # This is indented, so not a proper header

# Last H1 Header

Final content goes here.

## Conclusion

That's the end of our sample markdown file!"""


    def test_markdown_notitle(self):
        markdown = """## Not Main Title - This is an H1 Header

This is some introductory text under the main title. It contains regular paragraphs and some **bold text** and *italic text*.

## Section One - H2 Header

Here's content under the first section. This section talks about various topics.

### Subsection A - H3 Header

More detailed content here with some code examples:

```python
def hello_world():
    print("Hello, World!")
```

## Section Two - H2 Header

Another section with different content. This one has a list:

- Item one
- Item two  
- Item three

### Subsection B - H3 Header

## Another H2 Header in the Middle - Should not be Title

This demonstrates multiple H1 headers in the same document.

Some text with a [link](https://example.com) and an image reference.

## Final Section

#NotAHeader - this line doesn't start with # at beginning
  # This is indented, so not a proper header

## Last not H1 Header

Final content goes here.

## Conclusion

That's the end of our sample markdown file!"""
        with self.assertRaises(Exception) as context:
            extract_markdown(markdown)
        expected = "No Heading for Title"
        self.assertEqual(str(context.exception), expected)


if __name__ == "__main__":
    unittest.main()