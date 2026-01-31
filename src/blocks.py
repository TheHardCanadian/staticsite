from htmlnode import ParentNode,  text_node_to_html_node
from delimiter import text_to_textnodes
from textnode import TextNode, TextType
from enum import Enum
import re

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered list"
    ORDERED_LIST = "ordered list"


def split_blocks(document):
    split_docs = document.split("\n\n")
    #print(f"Split Docs before Strip: {split_docs}")
    blocks = []
    for block in split_docs: 
        if block.strip() != "":
            blocks.append(block.strip())
    return blocks

def block_to_block_type(block):
    if block.startswith(("# ","## ","### ","#### ","##### ","###### ")):
        return BlockType.HEADING
    elif block.startswith("```\n") and block.endswith("```\n"):
        return BlockType.CODE
    elif block.startswith("> "):
        return BlockType.QUOTE
    elif block.startswith("- "):
        return BlockType.UNORDERED_LIST
    elif re.match(r'^\d+\. ', block):
        return BlockType.ORDERED_LIST
    else:
        return BlockType.PARAGRAPH
    

def block_to_html_node(block):
    block_type = block_to_block_type(block)
    if block_type.value == "paragraph":
        return paragraph_to_html_node(block)
    if block_type.value == "heading":
        return heading_to_html_node(block)
    if block_type.value == "code":
        return code_to_html_node(block)
    if block_type.value == "ordered list":
        return olist_to_html_node(block)
    if block_type.value == "unordered list":
        return ulist_to_html_node(block)
    if block_type.value == "quote":
        return quote_to_html_node(block)

def text_to_children(text):   
    text_nodes = text_to_textnodes(text)
    children = []
    for text_node in text_nodes:
        html_node = text_node_to_html_node(text_node)
        children.append(html_node)
    return children

def paragraph_to_html_node(block):
    lines = block.split("\n")
    paragraph = " ".join(lines)
    children = text_to_children(paragraph)
    return ParentNode("p", children)

def heading_to_html_node(block):
    level = 0
    for char in block:
        if char == "#":
            level += 1
        else:
            break
    if level + 1 >= len(block):
        raise ValueError(f"Invalide heading level {level}")
    text = block[level + 1:]
    children = text_to_children(text)
    return ParentNode(f"h{level}", children)

def code_to_html_node(block):
    if not block.startswith("```") or not block.endswith("```"):
        raise ValueError("invalid code block")
    text = block[4:-3]
    raw_text_node = TextNode(text, TextType.PLAIN_TEXT)
    child = text_node_to_html_node(raw_text_node)
    code = ParentNode("code", [child])
    return ParentNode("pre", [code])

def olist_to_html_node(block):
    items = block.split("\n")
    html_items = []
    for item in items:
        parts = item.split(". ", 1)
        text = parts[1]
        children = text_to_children(text)
        html_items.append(ParentNode("li", children))
    return ParentNode("ol", html_items)

def ulist_to_html_node(block):
    items = block.split("\n")
    html_items = []
    for item in items:
        text = item[2:]
        children = text_to_children(text)
        html_items.append(ParentNode("li", children))
    return ParentNode("ul", html_items)

def quote_to_html_node(block):
    lines = block.split("\n")
    new_lines = []
    for line in lines:
        if not line.startswith(">"):
            raise ValueError("invalaid quote block")
        new_lines.append(line.lstrip(">").strip())
    content = " ".join(new_lines)
    children = text_to_children(content)
    return ParentNode("blockquote", children)


def markdown_to_html(markdown):
    blocks = split_blocks(markdown)
    children = []
    for block in blocks:
        html_node = block_to_html_node(block)
        children.append(html_node)
    return ParentNode("div", children, None)

def extract_markdown(markdown):
    h1 = re.search(r'^#\s+.*', markdown, re.MULTILINE)

    if h1 is None:
        raise Exception("No Heading for Title")
    
    print(h1.group())
    title = h1.group()
    title = title.lstrip('# ')
    print(title)
    return title


md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""

node = markdown_to_html(md)
html = node.to_html()
print(html)
#block = "#  A Tale of Two Cities"
#print(block_to_block_type(block))

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

print(extract_markdown(markdown))