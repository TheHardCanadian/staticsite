from enum import Enum

class TextType(Enum):
    PLAIN_TEXT = "plain"
    BOLD_TEXT = "bold"
    ITALIC_TEXT = "italic"
    CODE_TEXT = "code"
    LINK = "link"
    IMAGE = "image"

class TextNode:
    def __init__(self, text, text_type, url=None):
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, textnode2):
        if self.text == textnode2.text and self.text_type == textnode2.text_type and self.url == textnode2.url:
            #print("Good True Fantastic")
            return True
        else:
            return False    
        
    def __repr__(self):
        output_text = self.text.upper()
        output_type = self.text_type.value.upper()
        if self.url:
            output_url = self.url.upper()
            output_string = f"TextNode({output_text}, {output_type}, {output_url})"
        else:
            output_string = f"TextNode({output_text}, {output_type})"
        
        return output_string

