from textnode import TextNode, TextType


def split_nodes_delimiter(old_nodes, delimiter, text_type, closing_delimiter=None):
    
    delimiters = {'bold':["**", "__"],
                  "italic": ["*", "_"],
                  "code":["`"], 
                  "image":["!["], 
                  "link":["["]
    }

    closing_delimiters = {"image": "]",
                          "link": "]"
                          }
    
    #def delimit_string(inside_delimiter, new_nodes)
    if delimiter not in delimiters[text_type.value]:
        raise Exception("Delimiter error: Improper delimiter")
    if closing_delimiter:
        if text_type.value not in closing_delimiters:
            raise KeyError(f"Text type {text_type.value} does not support closing delimiters")
        if closing_delimiter != closing_delimiters[text_type.value]:
            raise Exception("Delimiter error: Improper closing delimiter")
            
    current_text = ""
    new_nodes = []
    inside_delimiter = False
    i=0
    while i < len(old_nodes):
        if closing_delimiter:
            if old_nodes[i:].startswith(closing_delimiter) and not inside_delimiter:
                raise Exception("Delimeter error: Closing delimeter not lead by opening delimeter")
            elif old_nodes[i:].startswith(delimiter) and inside_delimiter:
                raise Exception("Delimeter error: Delimeter not followed by closing delimeter")
            if old_nodes[i:].startswith(delimiter):
                #found delimeter
                if current_text: #this means if the string is not empty
                    node_type = text_type if inside_delimiter else TextType.PLAIN_TEXT
                    new_nodes.append(TextNode(current_text,node_type))
                    current_text = ""
                inside_delimiter = not inside_delimiter
                i += len(delimiter)

            elif old_nodes[i:].startswith(closing_delimiter):
                if current_text: #this means if the string is not empty
                    node_type = text_type if inside_delimiter else TextType.PLAIN_TEXT
                    new_nodes.append(TextNode(current_text,node_type))
                    current_text = ""
                inside_delimiter = not inside_delimiter
                i += len(closing_delimiter)

            else:
                current_text += old_nodes[i]
                i+=1
        elif closing_delimiter == None:
            if old_nodes[i:].startswith(delimiter):
                if current_text: #this means if the string is not empty
                    node_type = text_type if inside_delimiter else TextType.PLAIN_TEXT
                    new_nodes.append(TextNode(current_text,node_type))
                    current_text = ""
                inside_delimiter = not inside_delimiter
                i += len(delimiter)
            else:
                current_text += old_nodes[i]
                i+=1

    if current_text:
        node_type = text_type if inside_delimiter else TextType.PLAIN_TEXT
        new_nodes.append(TextNode(current_text,node_type))

    #print(new_nodes)
    return new_nodes
    

#split_nodes_delimiter("This is an ![IMAGE] that I'm trying to upload", "![", TextType.IMAGE,"]")
#bold = split_nodes_delimiter("This is some **bold text** that I'm trying to implement", "**", TextType.BOLD_TEXT)
#print(bold)
#split_nodes_delimiter("This is the text that I'm trying to _ACTION edit) for the test cycle", "_", TextType.ITALIC_TEXT, ")")    
#split_nodes_delimiter("This is the text that I'm trying to ![ACTION** edit) for the test cycle", "![", TextType.IMAGE, "**")
"""
GOAL - create TextNodes from Markdown strings

Not worry about nested inline elements.

Create a function that splits the old nodes, with delimeter and text type.

"""